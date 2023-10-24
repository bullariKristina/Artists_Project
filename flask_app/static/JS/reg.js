const mainSwitchBtn = document.querySelector('.form-tabs__slider'),
			signInSwitchBtn = document.querySelector('.form-tabs__btn_sign-in'),
			registerSwitchBtn = document.querySelector('.form-tabs__btn_register'),
			formLogin = document.querySelector('.form-login'),
			formRegister = document.querySelector('.form-register'),
			eyeShow = document.querySelectorAll('.form__eye[data-eye]'),
			formLoginPassword = document.querySelector('#form-login__password'),
			formRegisterPassword = document.querySelector('#form-register__password');
	signInSwitchBtn.addEventListener('click', () => { 
		formLogin.style.left = '0px';
		formRegister.style.right = '400px';
		mainSwitchBtn.style.left = '0px';
		registerSwitchBtn.style.color = '#000000';
		signInSwitchBtn.style.color = '#ECEFF1';
		formLoginPassword.dataset.eye = 'active'; 
		formRegisterPassword.dataset.eye = 'disable';
		switchActiveEye();
	});
	registerSwitchBtn.addEventListener('click', () => {
		formLogin.style.left = '400px';
		formRegister.style.right = '0px';
		mainSwitchBtn.style.left = '110px';
		registerSwitchBtn.style.color = '#ECEFF1';
		signInSwitchBtn.style.color = '#000000';
		formLoginPassword.dataset.eye = 'disable';
		formRegisterPassword.dataset.eye = 'active';
		switchActiveEye()
	});

	function switchActiveEye() { 
		eyeShow.forEach(e => {
			e.dataset.eye === 'active' ? e.dataset.eye = 'disable' : e.dataset.eye = 'active';
		})
	}

	
	document.querySelector('.authorisation').addEventListener('click', function (event) {
		let target = event.target;
		if (!target.classList.contains('form__eye')) return; 
		if (target.classList.contains('show')) {
			let activeEye = document.querySelectorAll('.form__eye[data-eye=active]');
			activeEye.forEach(e => {
				e.classList.toggle('show');
				e.classList.toggle('hide');
			});
			let activeFormLogin = document.querySelector('#form-login__password[data-eye=active]'),
					activeFormRegister = document.querySelector('#form-register__password[data-eye=active]');
			if (activeFormLogin) {
				if (activeFormLogin.getAttribute('type') === 'password') {
					activeFormLogin.setAttribute('type', 'text');
					return;
				}
				if (activeFormLogin.getAttribute('type') === 'text') {
					activeFormLogin.setAttribute('type', 'password');
					return;
				}
			}
			if (activeFormRegister) {
				if (activeFormRegister.getAttribute('type') === 'password') {
					activeFormRegister.setAttribute('type', 'text');
					return;
				}
				if (activeFormRegister.getAttribute('type') === 'text') {
					activeFormRegister.setAttribute('type', 'password');
					return;
				}
			}
		}
	});

	const formLoginInput = document.querySelectorAll('.form-login input:not([type=checkbox])'), 
			formRegisterInput = document.querySelectorAll('.form-register input:not([type=checkbox])');
	const loginCheckbox = document.querySelector('.form-login__checkbox'),
			registerCheckbox = document.querySelector('.form-register__checkbox');
	const formLoginBtn = document.querySelector('.form-login__btn'),
			formRegisterBtn = document.querySelector('.form-register__btn');

	let isFormValid = {}; 

	function switchCheckbox(elem) {
		if (elem.hasAttribute('checked')) {
			elem.removeAttribute('checked');
			isFormValid['checkBox'] = false;
			checkFormValid();
		} else {
			elem.setAttribute('checked', true);
			isFormValid['checkBox'] = true;
			checkFormValid();
		}
	}
	loginCheckbox.addEventListener('change', () => {
		switchCheckbox(loginCheckbox)
	});
	registerCheckbox.addEventListener('change', () => {
		switchCheckbox(registerCheckbox)
	});

	function checkFormValid() {
		if (isFormValid.text && isFormValid.email && isFormValid.password && isFormValid.checkBox) {
			formRegisterBtn.removeAttribute('disabled');
    }
		else {
			formRegisterBtn.setAttribute('disabled', 'disabled');
    }
	}

	formRegisterInput.forEach((elem) => {
		const regexEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

		elem.oninput = () => {
			if (elem.getAttribute('type') === 'text') {
				if (elem.value.length >= 3) {
					isFormValid.text = true;
					checkFormValid();
				} else {
					isFormValid['text'] = false;
					checkFormValid();
				}
			}
			if (elem.getAttribute('type') === 'email') {

				if (regexEmail.test(elem.value)) {
					isFormValid['email'] = true;
					checkFormValid();
				} else {
					isFormValid['email'] = false;
					checkFormValid();
				}
			}
			if (elem.getAttribute('type') === 'password') {

				if (elem.value.length >= 6) {
					isFormValid['password'] = true;
					checkFormValid();
				} else {
					isFormValid['password'] = false;
					checkFormValid();
				}
			}
		}
	});