document.addEventListener('DOMContentLoaded', () => {
    const FEATURES = [
        { api: 'Area', label: 'Diện tích' },
        { api: 'Perimeter', label: 'Chu vi' },
        { api: 'MajorAxisLength', label: 'Độ dài trục chính' },
        { api: 'MinorAxisLength', label: 'Độ dài trục phụ' },
        { api: 'AspectRatio', label: 'Tỷ lệ trục' },
        { api: 'Eccentricity', label: 'Độ lệch tâm' },
        { api: 'ConvexArea', label: 'Diện tích bao lồi' },
        { api: 'EquivDiameter', label: 'Đường kính tương đương' },
        { api: 'Extent', label: 'Tỷ lệ diện tích trong khung' },
        { api: 'Solidity', label: 'Độ đặc' },
        { api: 'Roundness', label: 'Độ tròn' },
        { api: 'Compactness', label: 'Độ gọn' },
        { api: 'ShapeFactor1', label: 'Hệ số hình dạng 1' },
        { api: 'ShapeFactor2', label: 'Hệ số hình dạng 2' },
        { api: 'ShapeFactor3', label: 'Hệ số hình dạng 3' },
        { api: 'ShapeFactor4', label: 'Hệ số hình dạng 4' }
    ];

    const form = document.getElementById('predict-form');
    const btnSubmit = document.getElementById('btn-submit');
    const btnClear = document.getElementById('btn-clear');
    
    const resultContainer = document.getElementById('result-container');
    const predictedClassEl = document.getElementById('predicted-class');
    const probabilitiesListEl = document.getElementById('probabilities-list');
    
    const errorContainer = document.getElementById('error-container');
    const errorMsgEl = document.getElementById('error-msg');

    if (form) {
        // 1. Generate Input Fields
        FEATURES.forEach((feature, index) => {
            const formGroup = document.createElement('div');
            formGroup.className = 'form-group';
            
            const label = document.createElement('label');
            label.setAttribute('for', feature.api);
            label.textContent = `${index + 1}. ${feature.label} (${feature.api})`;
            
            const input = document.createElement('input');
            input.type = 'number';
            input.step = 'any';
            input.id = feature.api;
            input.name = feature.api;
            input.required = true;
            
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            form.appendChild(formGroup);
        });

        // 2. Clear Form Event
        btnClear.addEventListener('click', () => {
            form.reset();
            hideResult();
            hideError();
        });

        // 3. Submit Event
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideResult();
            hideError();
            
            // Change button state
            const originalBtnText = btnSubmit.textContent;
            btnSubmit.textContent = 'Đang xử lý...';
            btnSubmit.disabled = true;

            try {
                // Collect data
                const requestData = {};
                for (const feature of FEATURES) {
                    const val = document.getElementById(feature.api).value;
                    if (!val) throw new Error(`Vui lòng nhập ${feature.label}`);
                    const numVal = parseFloat(val);
                    if (isNaN(numVal) || numVal <= 0) {
                        throw new Error(`${feature.label} phải là số lớn hơn 0.`);
                    }
                    requestData[feature.api] = numVal;
                }

                // Call API
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || data.details || 'Lỗi không xác định từ máy chủ.');
                }

                // Show result
                showResult(data.prediction, data.probabilities);

            } catch (err) {
                showError(err.message || 'Lỗi kết nối đến máy chủ.');
            } finally {
                btnSubmit.textContent = originalBtnText;
                btnSubmit.disabled = false;
            }
        });

        function showResult(prediction, probabilities) {
            predictedClassEl.textContent = prediction;
            
            // Render probabilities
            probabilitiesListEl.innerHTML = '';
            for (const [className, prob] of Object.entries(probabilities)) {
                const probItem = document.createElement('div');
                probItem.className = 'prob-item';
                if (className === prediction) {
                    probItem.classList.add('active');
                }
                
                const nameSpan = document.createElement('span');
                nameSpan.textContent = className;
                
                const valueSpan = document.createElement('span');
                valueSpan.textContent = `${(prob * 100).toFixed(2)}%`;
                
                probItem.appendChild(nameSpan);
                probItem.appendChild(valueSpan);
                probabilitiesListEl.appendChild(probItem);
            }

            resultContainer.classList.remove('hidden');
        }

        function hideResult() {
            resultContainer.classList.add('hidden');
        }

        function showError(msg) {
            errorMsgEl.textContent = msg;
            errorContainer.classList.remove('hidden');
        }

        function hideError() {
            errorContainer.classList.add('hidden');
        }
    }
});
