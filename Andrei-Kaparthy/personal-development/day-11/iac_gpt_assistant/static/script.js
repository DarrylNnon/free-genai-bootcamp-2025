document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('iac-form');
    const userRequestEl = document.getElementById('user-request');
    const resultContainer = document.getElementById('result-container');
    const loader = document.getElementById('loader');
    const outputGrid = document.getElementById('output-grid');
    const generatedCodeEl = document.getElementById('generated-code');
    const reportEl = document.getElementById('report');
    const copyCodeBtn = document.getElementById('copy-code-btn');
    const exampleBtns = document.querySelectorAll('.example-btn');

    const examplePrompts = {
        "Secure S3 Bucket": "Create a secure S3 bucket for private logs with versioning, server-side encryption, and public access block enabled.",
        "RDS Database": "Generate a terraform configuration for an AWS RDS mysql database that is not publicly accessible, has encryption at rest enabled, and has automated backups.",
        "EC2 Security Group": "Create a secure AWS security group for a web server that only allows HTTPS traffic from anywhere and SSH traffic from a specific IP address '1.2.3.4/32'."
    };

    // Handle example prompt buttons
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const promptText = examplePrompts[btn.textContent];
            if (promptText) {
                userRequestEl.value = promptText;
                userRequestEl.focus();
            }
        });
    });

    // Handle form submission
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const userRequest = userRequestEl.value;
        if (!userRequest.trim()) {
            alert('Please enter a request.');
            return;
        }

        // Show loader and hide previous results
        resultContainer.classList.remove('hidden');
        loader.classList.remove('hidden');
        outputGrid.classList.add('hidden');
        reportEl.innerHTML = ''; // Clear previous report
        generatedCodeEl.textContent = ''; // Clear previous code

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ request: userRequest }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An unknown error occurred on the server.');
            }

            const data = await response.json();

            // Display results
            generatedCodeEl.textContent = data.final_code || 'No code was generated.';
            // Use marked.js to parse markdown report
            reportEl.innerHTML = data.report_html ? marked.parse(data.report_html) : '<p>No report was generated.</p>';
            
            // Use highlight.js to apply syntax highlighting
            hljs.highlightElement(generatedCodeEl);
            
            outputGrid.classList.remove('hidden');

        } catch (error) {
            reportEl.innerHTML = `<p class="error"><strong>Error:</strong> ${error.message}</p>`;
            outputGrid.classList.remove('hidden'); // Show the grid to display the error
        } finally {
            loader.classList.add('hidden');
        }
    });

    // Handle copy code button
    copyCodeBtn.addEventListener('click', () => {
        const codeToCopy = generatedCodeEl.textContent;
        navigator.clipboard.writeText(codeToCopy).then(() => {
            copyCodeBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyCodeBtn.textContent = 'Copy Code';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy code: ', err);
            alert('Failed to copy code.');
        });
    });
});