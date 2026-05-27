// Configuración
const API_URL = 'http://localhost:8000/api/v1';

// Estado global
let datosGlobales = null;
let mesActual = new Date();
let vistaActual = 'mes'; // 'mes' o 'semana'

// Utilidades
function formatearFecha(fechaStr) {
    const fecha = new Date(fechaStr + 'T00:00:00');
    const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];

    return `${dias[fecha.getDay()]}, ${fecha.getDate()} de ${meses[fecha.getMonth()]}`;
}

function formatearFechaCorta(fechaStr) {
    const fecha = new Date(fechaStr + 'T00:00:00');
    const dias = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    return `${dias[fecha.getDay()]}, ${fecha.getDate()}/${fecha.getMonth() + 1}/${fecha.getFullYear()}`;
}

function obtenerNombreMes(mes) {
    const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    return meses[mes];
}

// Navegación entre pestañas
function switchTab(tabName) {
    // Ocultar todos los contenidos
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // Desactivar todas las pestañas
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Activar la pestaña seleccionada
    document.getElementById(`content-${tabName}`).classList.add('active');
    document.getElementById(`tab-${tabName}`).classList.add('active');

    // Si es calendario, renderizarlo
    if (tabName === 'calendario' && datosGlobales) {
        renderizarCalendario();
    }
}

// Cargar datos del backend
async function cargarDatos() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error').style.display = 'none';

    try {
        const [dashboardRes, hitosPerRes, hitosImpRes, calendarioRes] = await Promise.all([
            fetch(`${API_URL}/dashboard`),
            fetch(`${API_URL}/hitos-periodicos`),
            fetch(`${API_URL}/hitos-importantes`),
            fetch(`${API_URL}/calendario`)
        ]);

        if (!dashboardRes.ok) throw new Error('Error al cargar dashboard');

        const dashboard = await dashboardRes.json();
        const hitosPeriodicos = await hitosPerRes.json();
        const hitosImportantes = await hitosImpRes.json();
        const calendario = await calendarioRes.json();

        datosGlobales = {
            dashboard,
            hitosPeriodicos,
            hitosImportantes,
            calendario
        };

        renderizarDashboard(dashboard);

        document.getElementById('loading').style.display = 'none';
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'block';
        document.getElementById('error').className = 'error';
        document.getElementById('error').innerHTML = `
            <strong>❌ Error:</strong> No se pudo conectar con el backend.
            <br>Asegúrate de que el servidor esté corriendo en http://localhost:8000
            <br><small>${error.message}</small>
        `;
    }
}

// Renderizar Dashboard (TAB 1)
function renderizarDashboard(data) {
    // Posición Actual
    const posicion = data.posicionActual;
    document.getElementById('posicion-actual').innerHTML = `
        <div class="fecha-box today">
            <strong>Hoy es</strong><br>
            ${formatearFecha(posicion.fechaActual)}
        </div>
        <div class="posicion">
            <div class="dia-habil">
                <div class="dia-habil-label">Estamos en</div>
                <div class="dia-habil-numero">D+${posicion.diaHabilActual}</div>
            </div>
            <div class="arrow">→</div>
            <div class="dia-habil">
                <div class="dia-habil-label">Próximo día hábil</div>
                <div class="dia-habil-numero proximo">D+${posicion.proximoDiaHabil}</div>
            </div>
        </div>
        <div class="fecha-box">
            <strong>Próximo día hábil:</strong> ${formatearFechaCorta(posicion.fechaProximoDiaHabil)}
        </div>
    `;

    // Hitos Próximo Día
    document.getElementById('proximo-dia-titulo').textContent = `Para el D+${data.hitosProximoDia.diaHabil}`;
    const hitosProximo = data.hitosProximoDia.hitosPeriodicos;

    if (hitosProximo.length > 0) {
        document.getElementById('hitos-proximo-dia').innerHTML = hitosProximo.map(hito => `
            <div class="hito-item">
                <span class="check">✓</span>
                <div class="hito-content">
                    <div class="hito-title">${hito.accion}</div>
                </div>
            </div>
        `).join('');
    } else {
        document.getElementById('hitos-proximo-dia').innerHTML = `
            <p style="text-align: center; color: #6b7280; padding: 24px;">
                No hay hitos programados para este día
            </p>
        `;
    }

    // Feriados
    const feriados = data.feriadosProximos;
    if (feriados.length > 0) {
        document.getElementById('feriados').innerHTML = feriados.map(feriado => {
            const fecha = new Date(feriado.fecha + 'T00:00:00');
            const hoy = new Date();
            const dias = Math.ceil((fecha - hoy) / (1000 * 60 * 60 * 24));
            const texto = dias === 0 ? 'Hoy' : dias === 1 ? 'Mañana' : `En ${dias} días`;

            return `
                <div class="feriado-item">
                    <div class="feriado-content">
                        <div class="feriado-fecha">${formatearFechaCorta(feriado.fecha)}</div>
                        <div class="feriado-desc">${feriado.observaciones || 'Feriado'}</div>
                    </div>
                    <span class="badge red">${texto}</span>
                </div>
            `;
        }).join('');
    } else {
        document.getElementById('feriados').innerHTML = `<p style="text-align: center; color: #6b7280;">No hay feriados próximos</p>`;
    }

    // Hitos Importantes
    const hitosImp = data.hitosImportantesProximos;
    if (hitosImp.length > 0) {
        document.getElementById('hitos-importantes').innerHTML = hitosImp.map(hito => {
            const dias = hito.diasHastaHito;
            let badgeClass = 'blue';
            let texto = dias === 0 ? 'Hoy' : dias === 1 ? 'Mañana' : dias < 0 ? 'Pasado' : `En ${dias} días`;

            if (dias <= 7 && dias >= 0) badgeClass = 'red';
            else if (dias <= 14 && dias > 7) badgeClass = 'yellow';

            return `
                <div class="hito-item">
                    <div class="hito-content">
                        <div class="hito-title">${hito.titulo}</div>
                        <div class="hito-descripcion">${formatearFechaCorta(hito.fecha)}</div>
                    </div>
                    <span class="badge ${badgeClass}">${texto}</span>
                </div>
            `;
        }).join('');
    } else {
        document.getElementById('hitos-importantes').innerHTML = `<p style="text-align: center; color: #6b7280;">No hay hitos importantes próximos</p>`;
    }

    // Días restantes
    document.getElementById('dias-restantes').textContent =
        `${data.diasHabilesRestantesMes} días hábiles restantes en el mes`;
}

// Renderizar Calendario (TAB 2)
function renderizarCalendario() {
    if (vistaActual === 'mes') {
        renderizarCalendarioMensual();
    } else {
        renderizarCalendarioSemanal();
    }
}

function renderizarCalendarioMensual() {
    const año = mesActual.getFullYear();
    const mes = mesActual.getMonth();

    document.getElementById('month-title').textContent = `${obtenerNombreMes(mes)} ${año}`;

    // Obtener primer y último día del mes
    const primerDia = new Date(año, mes, 1);
    const ultimoDia = new Date(año, mes + 1, 0);

    // Calcular días a mostrar (incluyendo días del mes anterior/siguiente)
    const primerDiaSemana = primerDia.getDay(); // 0 = Domingo
    const diasMes = ultimoDia.getDate();

    const calendario = document.getElementById('calendario-mensual');
    calendario.innerHTML = '';

    // Headers de días
    const diasSemana = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    diasSemana.forEach(dia => {
        const header = document.createElement('div');
        header.className = 'calendar-day-header';
        header.textContent = dia;
        calendario.appendChild(header);
    });

    // Días del mes anterior (para completar la primera semana)
    const diasMesAnterior = new Date(año, mes, 0).getDate();
    for (let i = primerDiaSemana - 1; i >= 0; i--) {
        const dayDiv = crearDiaCalendario(año, mes - 1, diasMesAnterior - i, true);
        calendario.appendChild(dayDiv);
    }

    // Días del mes actual
    for (let dia = 1; dia <= diasMes; dia++) {
        const dayDiv = crearDiaCalendario(año, mes, dia, false);
        calendario.appendChild(dayDiv);
    }

    // Días del mes siguiente (para completar la última semana)
    const diasRestantes = 7 - (calendario.children.length - 7) % 7;
    if (diasRestantes < 7) {
        for (let dia = 1; dia <= diasRestantes; dia++) {
            const dayDiv = crearDiaCalendario(año, mes + 1, dia, true);
            calendario.appendChild(dayDiv);
        }
    }
}

function crearDiaCalendario(año, mes, dia, otroMes) {
    const fecha = new Date(año, mes, dia);
    const fechaStr = fecha.toISOString().split('T')[0];
    const hoy = new Date().toISOString().split('T')[0];

    const dayDiv = document.createElement('div');
    dayDiv.className = 'calendar-day';

    if (otroMes) {
        dayDiv.classList.add('other-month');
    }

    if (fechaStr === hoy) {
        dayDiv.classList.add('today');
    }

    // Buscar info del día en los datos
    const infoDia = buscarInfoDia(fechaStr);

    if (infoDia) {
        dayDiv.classList.add(infoDia.esHabil ? 'habil' : 'no-habil');
    }

    let html = `<div class="day-number">${dia}</div>`;

    if (infoDia) {
        // Mostrar D+X si es día hábil
        if (infoDia.diaHabilNumero) {
            html += `<div class="day-label">D+${infoDia.diaHabilNumero}</div>`;
        }

        // Mostrar feriado si aplica
        if (infoDia.esFeriado && infoDia.observaciones) {
            html += `<div class="day-hito feriado" title="${infoDia.observaciones}">🎉 ${infoDia.observaciones}</div>`;
        }

        // Hitos periódicos - agrupar por palabras clave
        if (infoDia.diaHabilNumero && datosGlobales) {
            const hitosDia = datosGlobales.hitosPeriodicos.filter(
                h => h.diaHabil === infoDia.diaHabilNumero
            );

            if (hitosDia.length > 0) {
                // Agrupar hitos por palabras clave (EERR, Reportes, etc.)
                const grupos = agruparHitos(hitosDia);

                if (grupos.length <= 3) {
                    // Mostrar todos si son pocos
                    hitosDia.forEach(hito => {
                        const textoCorto = truncarTexto(hito.accion, 25);
                        html += `<div class="day-hito" title="${hito.accion}">${textoCorto}</div>`;
                    });
                } else {
                    // Mostrar agrupados si son muchos
                    grupos.forEach(grupo => {
                        const texto = grupo.count > 1 ? `${grupo.nombre} (${grupo.count})` : grupo.nombre;
                        const titulos = grupo.hitos.map(h => h.accion).join('\n');
                        html += `<div class="day-hito" title="${titulos}">${texto}</div>`;
                    });
                }
            }
        }

        // Hitos importantes
        if (datosGlobales) {
            const hitosImportantesDia = datosGlobales.hitosImportantes.filter(
                h => h.fecha === fechaStr
            );
            hitosImportantesDia.forEach(hito => {
                const textoCorto = truncarTexto(hito.titulo, 20);
                html += `<div class="day-hito importante" title="${hito.titulo}">⭐ ${textoCorto}</div>`;
            });
        }
    }

    dayDiv.innerHTML = html;
    return dayDiv;
}

function agruparHitos(hitos) {
    // Agrupar hitos por palabras clave comunes
    const grupos = {};

    hitos.forEach(hito => {
        // Buscar palabra clave (primera palabra o sigla)
        const palabraClave = extraerPalabraClave(hito.accion);

        if (!grupos[palabraClave]) {
            grupos[palabraClave] = {
                nombre: palabraClave,
                count: 0,
                hitos: []
            };
        }

        grupos[palabraClave].count++;
        grupos[palabraClave].hitos.push(hito);
    });

    return Object.values(grupos);
}

function extraerPalabraClave(texto) {
    // Extraer siglas (EERR, BCRA, etc.) o primera palabra significativa
    const siglas = texto.match(/^[A-Z]{2,}/);
    if (siglas) return siglas[0];

    // O tomar hasta el primer espacio/guion/paréntesis
    const primera = texto.split(/[\s\-\(\)]/)[0];
    return primera || texto;
}

function truncarTexto(texto, maxLen) {
    if (texto.length <= maxLen) return texto;
    return texto.substring(0, maxLen - 3) + '...';
}

function renderizarCalendarioSemanal() {
    // Por ahora mostrar la semana actual
    const hoy = new Date();
    const diaSemana = hoy.getDay(); // 0 = Domingo

    // Calcular lunes de la semana actual
    const lunes = new Date(hoy);
    lunes.setDate(hoy.getDate() - (diaSemana === 0 ? 6 : diaSemana - 1));

    const semanal = document.getElementById('calendario-semanal');
    semanal.innerHTML = '';

    // Generar 5 días hábiles (lun-vie)
    for (let i = 0; i < 5; i++) {
        const fecha = new Date(lunes);
        fecha.setDate(lunes.getDate() + i);

        const card = crearDiaSemanal(fecha);
        semanal.appendChild(card);
    }
}

function crearDiaSemanal(fecha) {
    const fechaStr = fecha.toISOString().split('T')[0];
    const hoy = new Date().toISOString().split('T')[0];

    const card = document.createElement('div');
    card.className = 'week-day-card';

    if (fechaStr === hoy) {
        card.classList.add('today');
    }

    const infoDia = buscarInfoDia(fechaStr);

    const diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

    let html = `
        <div class="week-day-header">${diasSemana[fecha.getDay()]}</div>
        <div class="week-day-date">${fecha.getDate()}/${fecha.getMonth() + 1}/${fecha.getFullYear()}</div>
    `;

    if (infoDia && infoDia.diaHabilNumero) {
        html += `<div style="color: #0033A0; font-weight: 600; margin-bottom: 12px;">D+${infoDia.diaHabilNumero}</div>`;
    }

    html += `<div class="week-hito-list">`;

    if (infoDia) {
        if (infoDia.esFeriado) {
            const textoFeriado = infoDia.observaciones || 'Feriado';
            html += `<div class="hito-item"><span class="check">🎉</span><div class="hito-content"><div class="hito-title">${textoFeriado}</div></div></div>`;
        }

        // Hitos periódicos
        if (infoDia.diaHabilNumero && datosGlobales) {
            const hitosDia = datosGlobales.hitosPeriodicos.filter(
                h => h.diaHabil === infoDia.diaHabilNumero
            );
            hitosDia.forEach(hito => {
                html += `
                    <div class="hito-item">
                        <span class="check">✓</span>
                        <div class="hito-content">
                            <div class="hito-title">${hito.accion}</div>
                        </div>
                    </div>
                `;
            });
        }

        // Hitos importantes
        if (datosGlobales) {
            const hitosImportantesDia = datosGlobales.hitosImportantes.filter(
                h => h.fecha === fechaStr
            );
            hitosImportantesDia.forEach(hito => {
                html += `
                    <div class="hito-item">
                        <span class="check">⭐</span>
                        <div class="hito-content">
                            <div class="hito-title">${hito.titulo}</div>
                        </div>
                    </div>
                `;
            });
        }
    }

    if (!infoDia || ((!infoDia.esFeriado && !infoDia.diaHabilNumero))) {
        html += `<p style="color: #6b7280; font-size: 0.875rem;">Sin hitos programados</p>`;
    }

    html += `</div>`;

    card.innerHTML = html;
    return card;
}

function buscarInfoDia(fechaStr) {
    if (!datosGlobales || !datosGlobales.calendario) return null;

    // Buscar en el calendario completo
    const dia = datosGlobales.calendario.find(d => d.fecha === fechaStr);
    return dia || null;
}

// Controles del calendario
function cambiarMes(delta) {
    if (delta === 0) {
        mesActual = new Date(); // Volver a hoy
    } else {
        mesActual.setMonth(mesActual.getMonth() + delta);
    }
    renderizarCalendario();
}

function cambiarVista(vista) {
    vistaActual = vista;

    document.getElementById('btn-mes').classList.toggle('active', vista === 'mes');
    document.getElementById('btn-semana').classList.toggle('active', vista === 'semana');

    document.getElementById('calendario-mensual').style.display = vista === 'mes' ? 'grid' : 'none';
    document.getElementById('calendario-semanal').style.display = vista === 'semana' ? 'flex' : 'none';

    renderizarCalendario();
}

// Inicialización
cargarDatos();

// Auto-refresh cada 60 segundos
setInterval(cargarDatos, 60000);
