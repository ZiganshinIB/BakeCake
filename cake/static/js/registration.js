Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            RegSchema: {
                reg: (value) => {
                    if (value) {
                        return true;
                    }
                    return 'Поле не заполнено';
                },
                phone_format: (value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                code_format: (value) => {
                    const regex = /^[a-zA-Z0-9]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат кода нарушен';
                    }
                    return true;
                }
            },
            Step: 'Number',
            RegInput: '',
            Name: '',
            EnteredNumber: ''

        }
    },
    methods: {
        RegSubmit() {
            if (this.Step === 'Number') {
                const formData = new FormData();
                formData.append('phone_number', this.RegInput);
                formData.append('name', this.Name);
                const response = fetch(registerUrl, {
                    method: 'POST',
                    body: formData

                })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            throw new Error(errorData.detail || 'Ошибка при регистрации');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.errors) {
                        document.getElementById('NameError').innerText = data.errors;

                    }else {
                        this.Step = 'Code';
                        this.EnteredNumber = this.RegInput;
                        this.RegInput = '';
                        alert(data.code);
                    }


                })
                .catch(error => {
                    this.errorMessage = 'Ошибка при регистрации: ' + error.message;
                });
            }
            else if (this.Step === 'Code') {
                alert("Подтверждение PIN-кода")
                const formData = new FormData();
                formData.append('pin', this.RegInput); // Отправляем PIN-код
                const response = fetch(registerUrl, {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(errorData => {
                        throw new Error(errorData.detail || 'Ошибка при подтверждении PIN-кода');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Вход успешен:', data);
                    this.Step = 'Finish';
                    this.RegInput = 'Регистрация успешна';

                })
                .catch(error => {
                    this.errorMessage = 'Ошибка при подтверждении PIN-кода: ' + error.message;
                });
            }
            else {
                this.Reset()
            }
        },
        ToRegStep1() {
            this.Step = 'Number'
            this.RegInput = this.EnteredNumber
        },
        Reset() {
            this.Step = 'Number'
            this.RegInput = ''
            this.Name = ''
            EnteredNumber = ''
        }
    }
}).mount('#RegModal')