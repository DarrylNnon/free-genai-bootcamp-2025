document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('iac-form');
    const generateBtn = document.getElementById('generate-btn');
    const userRequestInput = document.getElementById('user-request');

    const resultsContainer = document.getElementById('results-container');
    const statusUpdates = document.getElementById('status-updates');
    const statusText = document.getElementById('status-text');
    const finalOutput = document.getElementById('final-output');
    const errorOutput = document.getElementById('error-output');
    const errorMessage = document.getElementById('error-message');

    const terraformCodeEl = document.getElementById('terraform-code');
    const reportOutputEl = document.getElementById('report-output');
    const copyCodeBtn = document.getElementById('copy-code-btn');

    const resetUI = () => {
        resultsContainer.classList.add('hidden');
        finalOutput.classList.add('hidden');
        errorOutput.classList.add('hidden');
        statusUpdates.classList.remove('hidden');
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate & Secure';
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userRequest = userRequestInput.value.trim();

        if (!userRequest) {
            alert('Please describe the infrastructure you need.');
            return;
        }

        // --- Start processing ---
        generateBtn.disabled = true;
        generateBtn.textContent = 'Processing...';
        resultsContainer.classList.remove('hidden');
        finalOutput.classList.add('hidden');
        errorOutput.classList.add('hidden');
        statusUpdates.classList.remove('hidden');
        statusText.textContent = 'Sending request to AI...';

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ request: userRequest }),
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'An unknown error occurred.');
            }

            // --- Display results ---
            statusUpdates.classList.add('hidden');

            if (result.error) {
                errorMessage.textContent = result.error;
                errorOutput.classList.remove('hidden');
            } else {
                terraformCodeEl.textContent = result.terraform_code;
                reportOutputEl.innerHTML = result.report_html;
                finalOutput.classList.remove('hidden');
            }

        } catch (err) {
            statusUpdates.classList.add('hidden');
            errorMessage.textContent = err.message;
            errorOutput.classList.remove('hidden');
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate & Secure';
        }
    });

    copyCodeBtn.addEventListener('click', () => {
        const code = terraformCodeEl.textContent;
        navigator.clipboard.writeText(code).then(() => {
            copyCodeBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyCodeBtn.textContent = 'Copy Code';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy code: ', err);
            alert('Failed to copy code to clipboard.');
        });
    });

    // Optional: Reset UI when user starts typing a new request
    userRequestInput.addEventListener('input', () => {
        if (!resultsContainer.classList.contains('hidden')) {
            resetUI();
        }
    });
});
