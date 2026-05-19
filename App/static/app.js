let customSvgDataUrl = null;
let copyTimeoutId = null;

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('menu-toggle-btn');
    const contentContainer = document.getElementById('content-container');

    if (!sidebar || !menuBtn || !contentContainer) return;

    sidebar.classList.toggle('hidden');
    menuBtn.classList.toggle('open');
    contentContainer.classList.toggle('menu-open');
}

function toggleLogoType(type) {
    const simpleDiv = document.getElementById('simple-logo');
    const customDiv = document.getElementById('custom-logo');
    const logoColorSection = document.getElementById('logo-color-section');
    const btnSimple = document.getElementById('btn-simple');
    const btnCustom = document.getElementById('btn-custom');
    const fileInput = document.getElementById('file');
    const logoInput = document.getElementById('logo');

    if (!simpleDiv || !customDiv || !logoColorSection || !btnSimple || !btnCustom) return;

    if (type === 'simple') {
        simpleDiv.classList.remove('hidden');
        customDiv.classList.add('hidden');
        logoColorSection.classList.remove('hidden');
        btnSimple.className = 'flex-1 px-3 py-2 text-xs rounded bg-purple-600/30 text-white border border-purple-500/20';
        btnCustom.className = 'flex-1 px-3 py-2 text-xs rounded bg-white/5 text-gray-400 border border-white/5';
        if (fileInput) {
            fileInput.removeAttribute('required');
            fileInput.value = '';
        }
        customSvgDataUrl = null;
        if (logoInput) logoInput.focus();
    } else {
        simpleDiv.classList.add('hidden');
        customDiv.classList.remove('hidden');
        logoColorSection.classList.add('hidden');
        btnSimple.className = 'flex-1 px-3 py-2 text-xs rounded bg-white/5 text-gray-400 border border-white/5';
        btnCustom.className = 'flex-1 px-3 py-2 text-xs rounded bg-purple-600/30 text-white border border-purple-500/20';
        if (fileInput) {
            fileInput.setAttribute('required', 'required');
            fileInput.focus();
        }
    }

    updateLivePreview();
}

function handleLabelColorSelect() {
    const select = document.getElementById('labelColor-select');
    const customWrapper = document.getElementById('labelColor-custom-wrapper');
    const hiddenInput = document.getElementById('labelColor');
    const picker = document.getElementById('labelColor-picker');
    const label = (document.getElementById('label') ? document.getElementById('label').value.trim() : '');
    const warningIcon = document.getElementById('label-warning-icon');

    if (!label && select.value !== '') {
        if (warningIcon) warningIcon.classList.remove('hidden');
        select.value = '';
        if (customWrapper) customWrapper.classList.add('hidden');
        if (hiddenInput) hiddenInput.value = '';
        updateLivePreview();
        return;
    }

    if (!select || !customWrapper || !hiddenInput) return;

    if (select.value === 'custom') {
        customWrapper.classList.remove('hidden');
        hiddenInput.value = (picker && picker.value) ? picker.value : '';
        if (picker && !picker._colorisInitialized) {
            Coloris({
                el: picker,
                theme: 'polaroid',
                themeMode: 'dark',
                alpha: false,
                format: 'hex',
                formatToggle: false,
                swatches: ['#44cc11','#97ca00','#dfb317','#fe7d37','#e05d44','#007ec6','#8a2be2','#333333','#555555','#ffffff','#000000']
            });
            picker._colorisInitialized = true;
        }
        if (picker) {
            picker.addEventListener('input', () => {
                hiddenInput.value = picker.value;
                updateLivePreview();
                checkLabelValidation();
            });
        }
    } else {
        customWrapper.classList.add('hidden');
        hiddenInput.value = select.value;
    }

    updateLivePreview();
    checkLabelValidation();
}

function handleLogoColorSelect() {
    const select = document.getElementById('logoColor-select');
    const customWrapper = document.getElementById('logoColor-custom-wrapper');
    const hiddenInput = document.getElementById('logoColor');
    const picker = document.getElementById('logoColor-picker');

    if (!select || !customWrapper || !hiddenInput) return;

    if (select.value === 'custom') {
        customWrapper.classList.remove('hidden');
        hiddenInput.value = (picker && picker.value) ? picker.value : '';
        if (picker && !picker._colorisInitialized) {
            Coloris({
                el: picker,
                theme: 'polaroid',
                themeMode: 'dark',
                alpha: false,
                format: 'hex',
                formatToggle: false,
                swatches: ['#44cc11','#97ca00','#dfb317','#fe7d37','#e05d44','#007ec6','#8a2be2','#333333','#555555','#ffffff','#000000']
            });
            picker._colorisInitialized = true;
        }
        if (picker) {
            picker.addEventListener('input', () => {
                hiddenInput.value = picker.value;
                updateLivePreview();
            });
        }
    } else {
        customWrapper.classList.add('hidden');
        hiddenInput.value = select.value;
    }

    updateLivePreview();
    checkLabelValidation();
}

function updateLivePreview() {
    const labelInput = document.getElementById('label');
    const messageInput = document.getElementById('message');
    const label = (labelInput ? labelInput.value.trim() : '') || labelInput?.placeholder || '';
    const message = (messageInput ? messageInput.value.trim() : '') || messageInput?.placeholder || 'message';
    const color = (document.getElementById('color') ? document.getElementById('color').value : 'brightgreen') || 'brightgreen';

    let badgeContent;
    if (label) {
        badgeContent = `${label}-${message}-${color}`;
    } else {
        badgeContent = `${message}-${color}`;
    }

    let url = `https://img.shields.io/badge/${badgeContent}`;
    const params = new URLSearchParams();

    const style = (document.getElementById('style') ? document.getElementById('style').value : '');
    if (style) params.append('style', style);

    const labelValue = labelInput ? labelInput.value.trim() : '';
    const labelColor = (document.getElementById('labelColor') ? document.getElementById('labelColor').value : '');
    if (labelColor && labelValue) params.append('labelColor', labelColor);

    const logoColor = (document.getElementById('logoColor') ? document.getElementById('logoColor').value : '');
    if (logoColor) params.append('logoColor', logoColor);

    const logoSize = (document.getElementById('logoSize') ? document.getElementById('logoSize').value : '');
    if (logoSize) params.append('logoSize', logoSize);

    const logoSimple = (document.getElementById('logo') ? document.getElementById('logo').value.trim() : '');
    if (customSvgDataUrl) {
        params.append('logo', customSvgDataUrl);
    } else if (logoSimple) {
        params.append('logo', logoSimple);
    }

    const queryString = params.toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;

    const livePreview = document.getElementById('live-preview');
    if (livePreview) {
        livePreview.src = fullUrl;
    }

    const liveUrl = document.getElementById('live-url');
    if (liveUrl) {
        liveUrl.dataset.rawUrl = fullUrl;
        applyOutputFormat();
    }
}

function applyOutputFormat() {
    const liveUrl = document.getElementById('live-url');
    const outputFormat = document.getElementById('output-format');
    if (!liveUrl || !outputFormat) return;

    const livePreview = document.getElementById('live-preview');
    const url = (livePreview && livePreview.src) ? livePreview.src : (liveUrl.dataset.rawUrl || liveUrl.textContent.split('\n')[0]);
    let formatted = url;

    if (outputFormat.value === 'markdown') {
        const alt = livePreview ? livePreview.alt : 'Badge';
        formatted = `![${alt}](${url})`;
    } else if (outputFormat.value === 'html') {
        const alt = livePreview ? livePreview.alt : 'Badge';
        formatted = `<img src="${url}" alt="${alt}">`;
    }

    liveUrl.textContent = formatted;
}

function checkLabelValidation() {
    const label = (document.getElementById('label') ? document.getElementById('label').value.trim() : '');
    const warningIcon = document.getElementById('label-warning-icon');
    if (!warningIcon) return;
    if (label) {
        warningIcon.classList.add('hidden');
    }
}

function copyLiveUrl(event) {
    const liveUrl = document.getElementById('live-url');
    const btn = document.querySelector('.copy-btn');
    if (!liveUrl || !btn) return;

    const url = liveUrl.textContent;
    const rect = btn.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    navigator.clipboard.writeText(url).then(() => {
        const existingLabel = btn.querySelector('.copied-label');
        if (existingLabel) existingLabel.remove();
        const existingFail = btn.querySelector('.copied-label');
        if (existingFail) existingFail.remove();
        btn.classList.add('is-copied');

        const label = document.createElement('span');
        label.className = 'copied-label';
        label.textContent = 'Copied!';
        btn.appendChild(label);

        btn.querySelectorAll('.copy-ripple').forEach((el) => el.remove());
        const ripple = document.createElement('span');
        ripple.className = 'copy-ripple';
        ripple.style.setProperty('--ripple-x', `${x}px`);
        ripple.style.setProperty('--ripple-y', `${y}px`);
        btn.appendChild(ripple);

        if (copyTimeoutId) clearTimeout(copyTimeoutId);
        copyTimeoutId = setTimeout(() => {
            const currentLabel = btn.querySelector('.copied-label');
            if (currentLabel) currentLabel.remove();
            btn.classList.remove('is-copied');
            copyTimeoutId = null;
        }, 1200);
    }).catch(() => {
        const existingLabel = btn.querySelector('.copied-label');
        if (existingLabel) existingLabel.remove();
        btn.classList.add('is-copied');

        const failed = document.createElement('span');
        failed.className = 'copied-label';
        failed.textContent = 'Copy failed';
        btn.appendChild(failed);

        if (copyTimeoutId) clearTimeout(copyTimeoutId);
        copyTimeoutId = setTimeout(() => {
            const currentFail = btn.querySelector('.copied-label');
            if (currentFail) currentFail.remove();
            btn.classList.remove('is-copied');
            copyTimeoutId = null;
        }, 1200);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const menuToggleBtn = document.getElementById('menu-toggle-btn');
    if (menuToggleBtn) {
        menuToggleBtn.addEventListener('click', toggleSidebar);
    }

    const menuCloseBtn = document.getElementById('menu-close-btn');
    if (menuCloseBtn) {
        menuCloseBtn.addEventListener('click', toggleSidebar);
    }

    const copyBtn = document.querySelector('.copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', copyLiveUrl);
    }

    const outputFormat = document.getElementById('output-format');
    if (outputFormat) {
        outputFormat.addEventListener('change', function() {
            applyOutputFormat();
        });
    }

    const btnSimple = document.getElementById('btn-simple');
    const btnCustom = document.getElementById('btn-custom');
    if (btnSimple) {
        btnSimple.addEventListener('click', () => toggleLogoType('simple'));
    }
    if (btnCustom) {
        btnCustom.addEventListener('click', () => toggleLogoType('custom'));
    }

    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) {
                customSvgDataUrl = null;
                updateLivePreview();
                return;
            }

            if (file.type !== 'image/svg+xml') {
                alert('Please select a valid SVG file');
                fileInput.value = '';
                customSvgDataUrl = null;
                updateLivePreview();
                return;
            }

            const reader = new FileReader();
            reader.onload = function(event) {
                try {
                    const svgContent = event.target.result;
                    const base64 = btoa(unescape(encodeURIComponent(svgContent)));
                    customSvgDataUrl = `data:image/svg+xml;base64,${base64}`;
                    updateLivePreview();
                } catch (error) {
                    alert('Error processing the SVG file');
                    fileInput.value = '';
                    customSvgDataUrl = null;
                    updateLivePreview();
                }
            };
            reader.onerror = function() {
                alert('Error reading the file');
                fileInput.value = '';
                customSvgDataUrl = null;
            };
            reader.readAsText(file);
        });
    }

    const inputs = ['label', 'message', 'color', 'style', 'logo', 'logoSize'];
    inputs.forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('input', () => {
                updateLivePreview();
                if (id === 'label') {
                    checkLabelValidation();
                }
            });
        }
    });

    const selects = ['labelColor-select', 'logoColor-select'];
    selects.forEach(id => {
        const select = document.getElementById(id);
        if (select && id === 'labelColor-select') {
            select.addEventListener('change', handleLabelColorSelect);
        } else if (select && id === 'logoColor-select') {
            select.addEventListener('change', handleLogoColorSelect);
        }
    });

    Coloris({
        el: '[data-coloris]',
        theme: 'polaroid',
        themeMode: 'dark',
        alpha: false,
        format: 'hex',
        formatToggle: false,
        swatches: ['#44cc11','#97ca00','#dfb317','#fe7d37','#e05d44','#007ec6','#8a2be2','#333333','#555555','#ffffff','#000000']
    });

    updateLivePreview();
});
