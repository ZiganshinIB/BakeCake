function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            schema1: {
                lvls: (value) => {
                    if (this.Levels) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value ) => {
                    if (this.Form) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (this.Topping) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-Я]+$/
                    if (!value) {
                        return true;
                    }
                    if (!regex.test(value)) {

                        return '⚠ Формат имени нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if (!regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format: (value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if (!regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },
            DATA: {},
            Costs: {
                Words: 0
            },
            Levels: null,
            Form: null,
            Topping: null,
            Berries: null,
            Decor: null,
            Words: null,
            Comments: null,
            Designed: false,

            Name: name,
            Phone: phone,
            Email: email,
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: null
        }
    },
    methods: {
        ToStep4() {
            console.log('step4')
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);
        },
        ToPay() {
            console.log('PAYMENT');

            let requestBody = {
                price: this.Cost,
                cake: {
                    level_id: this.Levels,
                    shape_id: this.Form,
                    topping_id: this.Topping,
                    berry_id: this.Berries,
                    decor_id: this.Decor
                },
                client: {
                    name: this.Name,
                    phone_number: this.Phone,
                    email: this.Email,
                    password: "11tryry5646451"
                },
                address: this.Address,
                delivery_date: this.Dates,
                delivered_at: this.Dates + ' ' + this.Time,
            };
            if (this.DelivComments) {
                requestBody.delivery_comments = this.DelivComments;
            }

            if (this.Comments) {
                requestBody.comment = this.Comments;
            }

            if (this.Words) {
                requestBody.inscription = this.Words;
            }
            const csrftoken = getCookie('csrftoken')
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = jQuery.trim(cookies[i]);
                        if (cookie.startsWith(name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break; // Выходим, как только найдём нужное cookie
                        }
                    }
                }
                return cookieValue;
            }
            const request = $.ajax({
                url: '/api/v1/order/',
                type: 'POST',
                data: JSON.stringify(requestBody),
                contentType: "application/json",
                headers: {
                    'X-CSRFToken': csrftoken // Установка CSRF-токена в заголовок
                },
                async: false,
                success: function (data) {
                    order = data;
                }
            });
            return order;
        }
    },
    computed: {
        Cost() {
            let price = 0;
            if (!this.Levels || !this.Form || !this.Topping) {
                return 0;
            }
            let requestBody = {
                level_id: this.Levels,
                shape_id: this.Form,
                topping_id: this.Topping,
                berry_id: this.Berries,
                decor_id: this.Decor,
            };
            const csrftoken = getCookie('csrftoken')
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = jQuery.trim(cookies[i]);
                        if (cookie.startsWith(name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break; // Выходим, как только найдём нужное cookie
                        }
                    }
                }
                return cookieValue;
            }
            const request = $.ajax({
                url: '/api/v1/calc/',
                type: 'POST',
                data: JSON.stringify(requestBody),
                headers: {
                    'X-CSRFToken': csrftoken // Установка CSRF-токена в заголовок
                },
                contentType: "application/json",
                async: false,
                success: function (data) {
                    price = data.price;
                }
            });
            return price;
        },
        Cake() {
            let requestBody = {
                level_id: this.Levels,
                shape_id: this.Form,
                topping_id: this.Topping
            };

            if (this.Berries) {
                requestBody.berry_id = this.Berries;
            }

            if (this.Decor) {
                requestBody.decor_id = this.Decor;
            }

            if (this.Words) {
                requestBody.label = this.Words;
            }
            const csrftoken = getCookie('csrftoken')
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = jQuery.trim(cookies[i]);
                        if (cookie.startsWith(name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break; // Выходим, как только найдём нужное cookie
                        }
                    }
                }
                return cookieValue;
            }
            const request = $.ajax({
                url: '/api/v1/cake/',
                type: 'GET',
                data: requestBody,
                contentType: "application/json",
                headers: {
                    'X-CSRFToken': csrftoken // Установка CSRF-токена в заголовок
                },
                async: false,
                success: function (data) {
                    cake = data;
                }
            });
            return cake;
        }
    }
}).mount('#VueApp')
