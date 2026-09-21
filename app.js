'use strict';
(() => {
  const fields = [...document.querySelectorAll('[data-edit]')];
  const defaults = Object.fromEntries(fields.map(el => [el.dataset.edit, el.textContent]));
  const storageKey = document.body.dataset.storageKey || 'arrc-winter-2026-poster-v1';
  const status = document.querySelector('#save-status');
  let editing = true;
  let currentTab = 'poster';
  let saveTimer;
  const values = () => Object.fromEntries(fields.map(el => [el.dataset.edit, el.textContent]));
  const apply = data => fields.forEach(el => { if (Object.hasOwn(data, el.dataset.edit) && typeof data[el.dataset.edit] === 'string') el.textContent = data[el.dataset.edit]; });
  const save = () => {
    clearTimeout(saveTimer);
    try { localStorage.setItem(storageKey, JSON.stringify(values())); status.textContent = '브라우저에 저장됨'; }
    catch { status.textContent = '자동 저장 불가 · 내용 저장을 이용하세요'; }
  };
  try { const saved = JSON.parse(localStorage.getItem(storageKey)); if (saved && typeof saved === 'object') apply(saved); }
  catch { status.textContent = '자동 저장을 사용할 수 없습니다'; }
  const setEditing = enabled => {
    editing = enabled;
    fields.forEach(el => { el.contentEditable = enabled ? 'plaintext-only' : 'false'; el.spellcheck = false; });
    const button = document.querySelector('#edit-toggle');
    button.textContent = enabled ? '편집 켜짐' : '미리보기';
    button.setAttribute('aria-pressed', String(enabled));
  };
  setEditing(true);
  fields.forEach(el => {
    el.addEventListener('input', () => { status.textContent = '저장 중…'; clearTimeout(saveTimer); saveTimer = setTimeout(save, 250); });
    el.addEventListener('paste', event => {
      event.preventDefault();
      const text = event.clipboardData.getData('text/plain');
      const selection = window.getSelection();
      if (!selection.rangeCount) return;
      const range = selection.getRangeAt(0);
      if (!el.contains(range.commonAncestorContainer)) return;
      range.deleteContents();
      const node = document.createTextNode(text);
      range.insertNode(node); range.setStartAfter(node); range.collapse(true);
      selection.removeAllRanges(); selection.addRange(range); save();
    });
    el.addEventListener('blur', () => { if (editing) save(); });
  });
  document.querySelector('#edit-toggle').addEventListener('click', () => setEditing(!editing));
  const tabs = [...document.querySelectorAll('[data-tab]')];
  const switchTab = name => {
    currentTab = name;
    tabs.forEach(button => {
      const selected = button.dataset.tab === name;
      button.setAttribute('aria-selected', String(selected)); button.tabIndex = selected ? 0 : -1;
      document.getElementById(`${button.dataset.tab}-panel`).hidden = !selected;
    });
    document.querySelector('#view-hint').textContent = name === 'reference' ? '제공된 원본 포스터입니다. 편집본과 내용·구성을 비교할 수 있습니다.' : name === 'review' ? '내부 검토 제안입니다. 각 항목과 확정할 사항을 클릭해 수정하세요.' : '문구를 클릭해 수정하세요. 변경 내용은 이 브라우저에 자동 저장됩니다.';
    document.querySelector('#edit-toggle').disabled = name === 'reference';
  };
  tabs.forEach((button, index) => {
    button.addEventListener('click', () => switchTab(button.dataset.tab));
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); switchTab(tabs[next].dataset.tab); tabs[next].focus(); }
    });
  });
  const download = (name, content, type) => {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = name; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
  };
  document.querySelector('#export-json').addEventListener('click', () => {
    save(); download('arrc-winter-program.json', JSON.stringify({ version: 1, fields: values() }, null, 2), 'application/json');
    status.textContent = '편집 내용 JSON 저장됨';
  });
  document.querySelector('#import').addEventListener('click', () => document.querySelector('#import-file').click());
  document.querySelector('#import-file').addEventListener('change', async event => {
    const file = event.target.files[0]; if (!file) return;
    try {
      if (file.size > 2000000) throw new Error('파일이 너무 큽니다');
      const data = JSON.parse(await file.text());
      if (data.version !== 1 || !data.fields || typeof data.fields !== 'object' || Array.isArray(data.fields)) throw new Error('파일 형식이 올바르지 않습니다');
      const entries = Object.entries(data.fields);
      if (!entries.length || entries.some(([key, value]) => !Object.hasOwn(defaults, key) || typeof value !== 'string' || value.length > 30000)) throw new Error('알 수 없는 필드 또는 잘못된 내용입니다');
      apply(data.fields); save(); status.textContent = '편집 내용을 불러왔습니다';
    } catch (error) { status.textContent = `불러오기 실패: ${error.message}`; }
    event.target.value = '';
  });
  document.querySelector('#reset').addEventListener('click', () => {
    if (window.confirm('포스터와 운영 검토의 모든 수정 내용을 처음 상태로 되돌릴까요? 보관하려면 먼저 내용 저장을 이용하세요.')) { apply(defaults); save(); }
  });
  document.querySelector('#print').addEventListener('click', () => { save(); window.print(); });
  document.querySelector('#export-html').addEventListener('click', async () => {
    const button = document.querySelector('#export-html'); button.disabled = true; status.textContent = 'HTML 내보내는 중…';
    try {
      save();
      const cssNode = document.querySelector('#app-style');
      const scriptNode = document.querySelector('#app-script');
      const read = async url => { const response = await fetch(url); if (!response.ok) throw new Error('파일 읽기 실패'); return response; };
      const imageUrls = [...new Set([...document.querySelectorAll('img')].map(img => img.src))];
      const [css, js, imageData] = await Promise.all([
        cssNode.tagName === 'LINK' ? read(cssNode.href).then(r => r.text()) : cssNode.textContent,
        scriptNode.src ? read(scriptNode.src).then(r => r.text()) : scriptNode.textContent,
        Promise.all(imageUrls.map(async url => [url, url.startsWith('data:') ? url : await read(url).then(r => r.blob()).then(blob => new Promise((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.onerror = reject; reader.readAsDataURL(blob); }))]))
      ]);
      const clone = document.documentElement.cloneNode(true);
      const style = document.createElement('style'); style.id = 'app-style'; style.textContent = css;
      clone.querySelector('#app-style').replaceWith(style);
      const script = document.createElement('script'); script.id = 'app-script'; script.textContent = js;
      clone.querySelector('#app-script').replaceWith(script);
      const embeddedImages = new Map(imageData);
      const originals = [...document.querySelectorAll('img')];
      clone.querySelectorAll('img').forEach((img, index) => img.src = embeddedImages.get(originals[index].src));
      clone.querySelector('body').dataset.storageKey = `arrc-export-${Date.now()}`;
      clone.querySelectorAll('[data-tab]').forEach(tab => { const selected = tab.dataset.tab === 'poster'; tab.setAttribute('aria-selected', String(selected)); tab.tabIndex = selected ? 0 : -1; });
      ['poster', 'review', 'reference'].forEach(name => { clone.querySelector(`#${name}-panel`).hidden = name !== 'poster'; });
      clone.querySelector('#export-html').disabled = false;
      clone.querySelector('#edit-toggle').disabled = false;
      clone.querySelector('#save-status').textContent = '로컬 편집 준비됨';
      clone.querySelector('#view-hint').textContent = '문구를 클릭해 수정하세요. 변경 내용은 이 브라우저에 자동 저장됩니다.';
      download('arrc-winter-program.html', '<!doctype html>\n' + clone.outerHTML, 'text/html;charset=utf-8');
      status.textContent = '독립 실행 HTML 저장됨';
    } catch (error) { status.textContent = 'HTML 저장 실패 · 로컬 서버에서 다시 시도하세요'; console.error(error); }
    finally { button.disabled = false; }
  });
  window.addEventListener('pagehide', save);
})();
