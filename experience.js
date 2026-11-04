// Presentation-only interactions. No requests, personal data, or CRM writes.
document.documentElement.classList.add('enhanced');
const controls = [...document.querySelectorAll('[data-scenario]')];
const panels = [...document.querySelectorAll('.demo-panel')];
function selectScenario(value) {
  controls.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.scenario === value)));
  panels.forEach(panel => { panel.hidden = panel.id !== `scenario-${value}`; });
  const action = document.querySelector('.demo-footer .btn');
  if (action) {
    const french = document.documentElement.lang === 'fr';
    action.href = value === '2' ? (french ? '/rfq-fr.html#rfq-audit' : '/rfq.html#rfq-audit') : '#contact';
    action.textContent = value === '2' ? (french ? 'Demander le bilan RFQ · 30 min' : 'Request the RFQ audit · 30 min') : (french ? 'Demander le bilan Web · 15 min' : 'Request the website review · 15 min');
  }
}
controls.forEach(button => button.addEventListener('click',()=>selectScenario(button.dataset.scenario)));
if (controls.length) selectScenario('0');
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('#site-links');
toggle?.addEventListener('click',()=>toggle.setAttribute('aria-expanded',String(toggle.getAttribute('aria-expanded')!=='true')));
links?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>toggle?.setAttribute('aria-expanded','false')));
document.addEventListener('keydown',event=>{
  if(event.key==='Escape') {
    if(toggle?.getAttribute('aria-expanded')==='true'){toggle.setAttribute('aria-expanded','false');toggle.focus();}
    document.querySelectorAll('.subnav[open]').forEach(menu=>{menu.open=false;menu.querySelector('summary')?.focus();});
  }
});
const frame=document.querySelector('.formbox iframe');
frame?.addEventListener('load',()=>{const status=document.querySelector('#form-status');if(status)status.textContent=status.dataset.loaded;});
