document.addEventListener('DOMContentLoaded', () => {
    // 1. Thống kê từ dữ liệu huấn luyện (train.csv)
    const FEATURES = [
        // 4 đặc trưng chủ đạo có slider
        {
            api: 'Area',
            label: 'Diện tích (Area)',
            hasSlider: true,
            min: 20464,
            max: 248424,
            mean: 53052,
            step: 50,
            defaultVal: 53052
        },
        {
            api: 'Perimeter',
            label: 'Chu vi (Perimeter)',
            hasSlider: true,
            min: 524.7,
            max: 1921.7,
            mean: 854.7,
            step: 1,
            defaultVal: 854.7
        },
        {
            api: 'MajorAxisLength',
            label: 'Độ dài trục chính (MajorAxisLength)',
            hasSlider: true,
            min: 184.0,
            max: 738.1,
            mean: 319.8,
            step: 0.5,
            defaultVal: 319.8
        },
        {
            api: 'MinorAxisLength',
            label: 'Độ dài trục phụ (MinorAxisLength)',
            hasSlider: true,
            min: 122.5,
            max: 460.2,
            mean: 202.4,
            step: 0.5,
            defaultVal: 202.4
        },

        // 12 đặc trưng còn lại (nhập số chính xác)
        { api: 'AspectRatio', label: 'Tỷ lệ trục (AspectRatio)', min: 1.0364, max: 2.4303, mean: 1.5804 },
        { api: 'Eccentricity', label: 'Độ lệch tâm (Eccentricity)', min: 0.2628, max: 0.9114, mean: 0.7500 },
        { api: 'ConvexArea', label: 'Diện tích bao lồi (ConvexArea)', min: 20772, max: 251082, mean: 53771 },
        { api: 'EquivDiameter', label: 'Đường kính tương đương (EquivDiameter)', min: 161.4, max: 562.4, mean: 253.0 },
        { api: 'Extent', label: 'Tỷ lệ trong khung (Extent)', min: 0.5553, max: 0.8662, mean: 0.7499 },
        { api: 'Solidity', label: 'Độ đặc (Solidity)', min: 0.9446, max: 0.9947, mean: 0.9872 },
        { api: 'Roundness', label: 'Độ tròn (Roundness)', min: 0.5568, max: 0.9907, mean: 0.8741 },
        { api: 'Compactness', label: 'Độ gọn (Compactness)', min: 0.6406, max: 0.9816, mean: 0.8005 },
        { api: 'ShapeFactor1', label: 'Hệ số hình dạng 1 (ShapeFactor1)', min: 0.0028, max: 0.0105, mean: 0.0066 },
        { api: 'ShapeFactor2', label: 'Hệ số hình dạng 2 (ShapeFactor2)', min: 0.0006, max: 0.0037, mean: 0.0017 },
        { api: 'ShapeFactor3', label: 'Hệ số hình dạng 3 (ShapeFactor3)', min: 0.4103, max: 0.9636, mean: 0.6446 },
        { api: 'ShapeFactor4', label: 'Hệ số hình dạng 4 (ShapeFactor4)', min: 0.9500, max: 0.9997, mean: 0.9951 }
    ];

    // Mẫu ví dụ thực tế lấy từ tập dữ liệu huấn luyện
    const SAMPLE_PRESETS = [
        {
            className: 'SEKER',
            label: 'Seker',
            data: {
                Area: 40154.0, Perimeter: 729.638, MajorAxisLength: 241.2846, MinorAxisLength: 211.9747,
                AspectRatio: 1.1383, Eccentricity: 0.4777, ConvexArea: 40559.0, EquivDiameter: 226.1098,
                Extent: 0.7666, Solidity: 0.99, Roundness: 0.9478, Compactness: 0.9371,
                ShapeFactor1: 0.006, ShapeFactor2: 0.0029, ShapeFactor3: 0.8782, ShapeFactor4: 0.9996
            }
        },
        {
            className: 'BARBUNYA',
            label: 'Barbunya',
            data: {
                Area: 68648.0, Perimeter: 1004.91, MajorAxisLength: 347.2564, MinorAxisLength: 252.6546,
                AspectRatio: 1.3744, Eccentricity: 0.686, ConvexArea: 69720.0, EquivDiameter: 295.644,
                Extent: 0.7289, Solidity: 0.9846, Roundness: 0.8542, Compactness: 0.8514,
                ShapeFactor1: 0.0051, ShapeFactor2: 0.0016, ShapeFactor3: 0.7248, ShapeFactor4: 0.9962
            }
        },
        {
            className: 'BOMBAY',
            label: 'Bombay',
            data: {
                Area: 166654.0, Perimeter: 1529.386, MajorAxisLength: 572.6117, MinorAxisLength: 372.546,
                AspectRatio: 1.537, Eccentricity: 0.7594, ConvexArea: 168540.0, EquivDiameter: 460.6414,
                Extent: 0.7267, Solidity: 0.9888, Roundness: 0.8953, Compactness: 0.8045,
                ShapeFactor1: 0.0034, ShapeFactor2: 0.0009, ShapeFactor3: 0.6472, ShapeFactor4: 0.9947
            }
        },
        {
            className: 'CALI',
            label: 'Cali',
            data: {
                Area: 95159.0, Perimeter: 1187.813, MajorAxisLength: 456.6403, MinorAxisLength: 269.9497,
                AspectRatio: 1.6916, Eccentricity: 0.8066, ConvexArea: 97517.0, EquivDiameter: 348.0807,
                Extent: 0.7217, Solidity: 0.9758, Roundness: 0.8475, Compactness: 0.7623,
                ShapeFactor1: 0.0048, ShapeFactor2: 0.001, ShapeFactor3: 0.581, ShapeFactor4: 0.9829
            }
        },
        {
            className: 'HOROZ',
            label: 'Horoz',
            data: {
                Area: 40101.0, Perimeter: 782.797, MajorAxisLength: 312.0999, MinorAxisLength: 164.0728,
                AspectRatio: 1.9022, Eccentricity: 0.8507, ConvexArea: 40619.0, EquivDiameter: 225.9606,
                Extent: 0.7106, Solidity: 0.9872, Roundness: 0.8224, Compactness: 0.724,
                ShapeFactor1: 0.0078, ShapeFactor2: 0.0013, ShapeFactor3: 0.5242, ShapeFactor4: 0.9971
            }
        },
        {
            className: 'SIRA',
            label: 'Sira',
            data: {
                Area: 50040.0, Perimeter: 859.211, MajorAxisLength: 334.2318, MinorAxisLength: 191.4404,
                AspectRatio: 1.7459, Eccentricity: 0.8197, ConvexArea: 50663.0, EquivDiameter: 252.4142,
                Extent: 0.7864, Solidity: 0.9877, Roundness: 0.8518, Compactness: 0.7552,
                ShapeFactor1: 0.0067, ShapeFactor2: 0.0013, ShapeFactor3: 0.5703, ShapeFactor4: 0.9957
            }
        },
        {
            className: 'DERMASON',
            label: 'Dermason',
            data: {
                Area: 36216.0, Perimeter: 702.047, MajorAxisLength: 261.094, MinorAxisLength: 177.1601,
                AspectRatio: 1.4738, Eccentricity: 0.7346, ConvexArea: 36571.0, EquivDiameter: 214.7362,
                Extent: 0.7746, Solidity: 0.9903, Roundness: 0.9234, Compactness: 0.8224,
                ShapeFactor1: 0.0072, ShapeFactor2: 0.002, ShapeFactor3: 0.6764, ShapeFactor4: 0.9969
            }
        }
    ];

    const form = document.getElementById('predict-form');
    const primaryGrid = document.getElementById('primary-features-grid');
    const secondaryGrid = document.getElementById('secondary-features-grid');
    const presetButtonsContainer = document.getElementById('preset-buttons');
    const btnRandomSample = document.getElementById('btn-random-sample');

    const btnSubmit = document.getElementById('btn-submit');
    const btnClear = document.getElementById('btn-clear');
    
    const resultContainer = document.getElementById('result-container');
    const predictedClassEl = document.getElementById('predicted-class');
    const probabilitiesListEl = document.getElementById('probabilities-list');
    
    const errorContainer = document.getElementById('error-container');
    const errorMsgEl = document.getElementById('error-msg');

    if (form) {
        // 2. Render UI các trường nhập liệu
        FEATURES.forEach((feature, index) => {
            const formGroup = document.createElement('div');
            formGroup.className = feature.hasSlider ? 'form-group form-group-slider' : 'form-group';

            // Nhãn
            const labelRow = document.createElement('div');
            labelRow.className = 'label-row';

            const label = document.createElement('label');
            label.setAttribute('for', feature.api);
            label.textContent = `${index + 1}. ${feature.label}`;
            labelRow.appendChild(label);
            formGroup.appendChild(labelRow);

            // Ô nhập số
            const inputNumber = document.createElement('input');
            inputNumber.type = 'number';
            inputNumber.step = 'any';
            inputNumber.id = feature.api;
            inputNumber.name = feature.api;
            inputNumber.className = 'feature-input';
            inputNumber.required = true;
            inputNumber.placeholder = `VD: ${feature.mean}`;

            // Nếu là trường có slider
            if (feature.hasSlider) {
                const sliderRow = document.createElement('div');
                sliderRow.className = 'slider-row';

                const slider = document.createElement('input');
                slider.type = 'range';
                slider.id = `${feature.api}-slider`;
                slider.className = 'feature-slider';
                slider.min = feature.min;
                slider.max = feature.max;
                slider.step = feature.step || 1;
                slider.value = feature.mean;

                // Đồng bộ hai chiều (Two-way binding)
                // Kéo slider -> cập nhật ô số
                slider.addEventListener('input', () => {
                    inputNumber.value = slider.value;
                });

                // Nhập ô số -> đồng bộ slider nếu trong khoảng
                inputNumber.addEventListener('input', () => {
                    const val = parseFloat(inputNumber.value);
                    if (!isNaN(val)) {
                        if (val >= feature.min && val <= feature.max) {
                            slider.value = val;
                        } else if (val < feature.min) {
                            slider.value = feature.min;
                        } else {
                            slider.value = feature.max;
                        }
                    }
                });

                formGroup.appendChild(inputNumber);
                sliderRow.appendChild(slider);
                formGroup.appendChild(sliderRow);
                primaryGrid.appendChild(formGroup);
            } else {
                formGroup.appendChild(inputNumber);
                secondaryGrid.appendChild(formGroup);
            }

            // Dòng thông tin tham khảo từ tập huấn luyện
            const hint = document.createElement('span');
            hint.className = 'feature-hint';
            const formatReferenceValue = value => value.toLocaleString(undefined, {
                maximumFractionDigits: 9
            });
            hint.textContent = `Tham khảo: ${formatReferenceValue(feature.min)} – ${formatReferenceValue(feature.max)} (TB: ${formatReferenceValue(feature.mean)})`;
            formGroup.appendChild(hint);
        });

        // 3. Render các nút mẫu có sẵn (Presets)
        SAMPLE_PRESETS.forEach(preset => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn-preset';
            btn.textContent = `Mẫu ${preset.label}`;
            btn.title = `Nạp dữ liệu mẫu ví dụ cho giống ${preset.label}`;
            btn.addEventListener('click', () => {
                applySampleData(preset.data);
            });
            presetButtonsContainer.appendChild(btn);
        });

        // 4. Sự kiện nút mẫu ngẫu nhiên
        if (btnRandomSample) {
            btnRandomSample.addEventListener('click', () => {
                const randomIndex = Math.floor(Math.random() * SAMPLE_PRESETS.length);
                const randomPreset = SAMPLE_PRESETS[randomIndex];
                applySampleData(randomPreset.data);
            });
        }

        // Hàm điền dữ liệu mẫu vào 16 ô và đồng bộ slider
        function applySampleData(data) {
            FEATURES.forEach(feature => {
                const input = document.getElementById(feature.api);
                if (input && data[feature.api] !== undefined) {
                    input.value = data[feature.api];

                    if (feature.hasSlider) {
                        const slider = document.getElementById(`${feature.api}-slider`);
                        if (slider) {
                            slider.value = data[feature.api];
                        }
                    }
                }
            });
            hideResult();
            hideError();
        }

        // 5. Sự kiện nút Xóa dữ liệu / Đặt lại (Clear Form)
        btnClear.addEventListener('click', () => {
            form.reset();
            // Reset các slider về giá trị mặc định
            FEATURES.forEach(feature => {
                if (feature.hasSlider) {
                    const slider = document.getElementById(`${feature.api}-slider`);
                    if (slider) {
                        slider.value = feature.mean;
                    }
                }
            });
            hideResult();
            hideError();
        });

        // 6. Sự kiện Submit gửi dữ liệu đến /api/predict
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideResult();
            hideError();

            const originalBtnText = btnSubmit.textContent;
            btnSubmit.textContent = 'Đang phân loại...';
            btnSubmit.disabled = true;

            try {
                // Thu thập và kiểm tra dữ liệu đầu vào
                const requestData = {};
                for (const feature of FEATURES) {
                    const input = document.getElementById(feature.api);
                    const val = input ? input.value.trim() : '';
                    if (!val) {
                        throw new Error(`Vui lòng nhập giá trị cho: ${feature.label}`);
                    }
                    const numVal = parseFloat(val);
                    if (isNaN(numVal) || !isFinite(numVal) || numVal <= 0) {
                        throw new Error(`Đặc trưng "${feature.label}" phải là số hữu hạn lớn hơn 0.`);
                    }
                    requestData[feature.api] = numVal;
                }

                // Gửi request API
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

                // Hiển thị kết quả
                showResult(data.prediction, data.probabilities);

            } catch (err) {
                showError(err.message || 'Lỗi kết nối đến máy chủ.');
            } finally {
                btnSubmit.textContent = originalBtnText;
                btnSubmit.disabled = false;
            }
        });

        // 7. Các hàm tiện ích hiển thị kết quả và lỗi
        function showResult(prediction, probabilities) {
            predictedClassEl.textContent = prediction;

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
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
