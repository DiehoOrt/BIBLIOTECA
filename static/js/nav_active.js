// ================================================================
// Proyecto:  SGBU — Sistema de Gestión Bibliotecaria UNICAES
// Versión:   1.0.0
// País:      El Salvador
// Año:       2026
// Empresa:   InnoByte
// Autores:   Jonathan Fuentes Henriquez, Andrew Enrique Mercado,
//            Hector Jhosue Ramos, Enzo Howard Rivera,
//            Diego Josue Ortiz, Alejandra Marisol,
//            Nathaly Portillo, Roberto Leonel Dominguez
// Licencia:  MIT License
// ================================================================
document.addEventListener('DOMContentLoaded', function () {
    const current = window.location.pathname;

    // Recopilar todos los links con su href
    const links = Array.from(
        document.querySelectorAll('#sidebarNav .nav-item .nav-link')
    ).filter(link => {
        const href = link.getAttribute('href');
        return href && href !== '#' && href !== '/';
    });

    // Quedarse solo con el match más específico (href más largo que sea prefijo)
    const best = links
        .filter(link => current === link.getAttribute('href') || current.startsWith(link.getAttribute('href')))
        .sort((a, b) => b.getAttribute('href').length - a.getAttribute('href').length)[0];

    if (best) best.closest('.nav-item').classList.add('active');
});
