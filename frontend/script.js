document.addEventListener('DOMContentLoaded', () => {

    // Feature Tabs Logic (Text, File, URL)
    const tabBtns = document.querySelectorAll('.tab-btn');
    const inputPanels = document.querySelectorAll('.input-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            tabBtns.forEach(b => b.classList.remove('active'));
            inputPanels.forEach(p => p.style.display = 'none');

            // Add active to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).style.display = 'block';
        });
    });

    // Segmented Logic (Length options)
    const segments = document.querySelectorAll('.segment');
    segments.forEach(seg => {
        seg.addEventListener('click', () => {
            document.querySelectorAll('.segment').forEach(s => s.classList.remove('active'));
            seg.classList.add('active');
        });
    });

    // Clear Button
    const clearBtn = document.querySelector('.clear-btn');
    const textarea = document.querySelector('textarea');
    if (clearBtn && textarea) {
        clearBtn.addEventListener('click', () => {
            textarea.value = '';
        });
    }

    // Generate Button Logic
    const generateBtn = document.getElementById('generateBtn');
    const resultArea = document.getElementById('resultArea');
    const loadingState = document.getElementById('loadingState');
    const finalOutput = document.getElementById('finalOutput');
    const btnText = generateBtn.querySelector('.btn-text');
    const btnIcon = generateBtn.querySelector('i');

    generateBtn.addEventListener('click', () => {
        // Change button state
        btnText.innerText = "Đang xử lý...";
        btnIcon.className = "fa-solid fa-spinner fa-spin";
        generateBtn.style.opacity = '0.8';
        generateBtn.style.pointerEvents = 'none';

        // Show result area with loading skeleton
        resultArea.style.display = 'block';
        loadingState.style.display = 'block';
        finalOutput.style.display = 'none';

        // Scroll to result smoothly
        setTimeout(() => {
            resultArea.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }, 100);

        // Mock API Call (2.5 seconds)
        setTimeout(() => {
            // Restore button
            btnText.innerText = "Tạo tóm tắt";
            btnIcon.className = "fa-solid fa-bolt";
            generateBtn.style.opacity = '1';
            generateBtn.style.pointerEvents = 'auto';

            // Switch to Final Output
            loadingState.style.display = 'none';
            finalOutput.style.display = 'block';
        }, 2500);
    });

    // Copy Button & Toast
    const copyBtn = document.querySelector('.copy-btn');
    const toast = document.getElementById('toast');

    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            // Show toast
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        });
    }

});
