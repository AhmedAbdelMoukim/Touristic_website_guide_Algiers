/* Petites interactions, sans dépendance autre que Bootstrap local. */
'use strict';
document.addEventListener('DOMContentLoaded', () => {
  // Galerie : filtre accessible et compteur mis à jour.
  const filters = document.querySelectorAll('[data-filter]');
  const photos = document.querySelectorAll('.gallery-item');
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(item => {
      const selected = item === button;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    let visible = 0;
    photos.forEach(photo => {
      photo.hidden = button.dataset.filter !== 'all' && photo.dataset.category !== button.dataset.filter;
      if (!photo.hidden) visible++;
    });
    document.querySelector('#gallery-count').textContent = visible + (visible === 1 ? ' photographie' : ' photographies');
  }));

  // Bootstrap gère le focus, Échap et le retour au bouton d'ouverture.
  document.querySelector('#photo-modal')?.addEventListener('show.bs.modal', event => {
    const source = event.relatedTarget;
    if (!source) return;
    const image = document.querySelector('#photo-large');
    image.src = source.dataset.src;
    image.alt = source.dataset.alt;
    document.querySelector('#photo-title').textContent = source.dataset.title;
    document.querySelector('#photo-description').textContent = source.dataset.alt;
  });

  // Bonus Web Storage : seuls les noms de lieux sont mémorisés.
  const storageKey = 'alger-la-blanche-carnet-v1';
  const buttons = [...document.querySelectorAll('.save-place')];
  const allowed = new Set(buttons.map(button => button.dataset.place));
  let favorites = [];
  let storageAvailable = true;
  if (buttons.length) {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || '[]');
      favorites = Array.isArray(saved) ? [...new Set(saved.filter(name => allowed.has(name)))] : [];
    } catch { storageAvailable = false; }
    const render = () => {
      buttons.forEach(button => {
        const selected = favorites.includes(button.dataset.place);
        button.setAttribute('aria-pressed', String(selected));
        button.textContent = selected ? '✓ Dans mon carnet — retirer' : '＋ Ajouter à mon carnet';
      });
      const list = document.querySelector('#saved-list');
      list.replaceChildren();
      favorites.forEach(name => {
        const item = document.createElement('li');
        item.textContent = name;
        list.append(item);
      });
      document.querySelector('#saved-empty').hidden = favorites.length > 0;
      document.querySelector('#clear-saved').hidden = favorites.length === 0;
      if (!storageAvailable) document.querySelector('#storage-note').textContent = 'Le stockage est indisponible. Votre carnet reste utilisable sur cette page, mais ne sera pas conservé après rechargement.';
    };
    const persist = () => {
      try { localStorage.setItem(storageKey, JSON.stringify(favorites)); }
      catch { storageAvailable = false; }
      render();
    };
    buttons.forEach(button => button.addEventListener('click', () => {
      const name = button.dataset.place;
      const present = favorites.includes(name);
      favorites = present ? favorites.filter(item => item !== name) : [...favorites, name];
      persist();
      document.querySelector('#save-status').textContent = name + (present ? ' retiré de votre carnet.' : ' ajouté à votre carnet.');
    }));
    document.querySelector('#clear-saved').addEventListener('click', () => {
      favorites = [];
      persist();
      document.querySelector('#save-status').textContent = 'Votre carnet a été vidé.';
    });
    render();
  }

  // Le navigateur assure la validation HTML5, aucune donnée n'est envoyée.
  const form = document.querySelector('#visit-form');
  if (form) {
    const date = document.querySelector('#visit-date');
    const now = new Date();
    date.min = [now.getFullYear(), String(now.getMonth() + 1).padStart(2, '0'), String(now.getDate()).padStart(2, '0')].join('-');
    ['full-name', 'message'].forEach(id => {
      const field = document.getElementById(id);
      field.addEventListener('input', () => {
        const min = field.minLength;
        field.setCustomValidity(field.value.trim().length < min ? 'Veuillez saisir au moins ' + min + ' caractères, hors espaces aux extrémités.' : '');
      });
    });
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      document.querySelector('#form-summary').textContent = 'Merci ' + String(data.get('nom')).trim() + '. Votre envie : ' + data.get('type') + ', pour ' + String(data.get('duree')).toLowerCase() + '.';
      const confirmation = document.querySelector('#form-success');
      confirmation.hidden = false;
      confirmation.focus();
    });
    form.addEventListener('input', () => { document.querySelector('#form-success').hidden = true; });
  }
});
