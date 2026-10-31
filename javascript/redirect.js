const routes = {aboutus:'aboutus', resources:'resources', faq:'faq', getinvolved:'getinvolved'};
const parts = location.pathname.split('/').filter(Boolean);
const page = parts.at(-1) === 'index.html' ? parts.at(-2) : parts.at(-1);
if (routes[page]) {
 const count = parts.at(-1) === 'index.html' ? 2 : 1;
 const base = '/' + parts.slice(0, -count).join('/');
 location.replace(base.replace(/\/$/, '') + '/html/' + routes[page] + '.html' + location.search + location.hash);
}
