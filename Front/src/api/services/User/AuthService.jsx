import axios from 'axios';
import axiosInstance from '../AxiosInstance'; 
const registerUserBuyerService = async (buyerData) => {
    const validBuyerData = {
        name: buyerData.name,
        surname: buyerData.surname,
        email: buyerData.email,
        dni: buyerData.dni,
        password: buyerData.password,
        eco_points: 0,
        billing_address: buyerData.billing_address,
        payment_method: 'Credit Card', 
        birth_date: buyerData.birth_date
    };
    try {
        const response = await axiosInstance.post('/buyers', validBuyerData);
        console.log('Registro de comprador exitoso', response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al registrar al comprador:', error.response ? error.response.data : error);
        throw error;
    }
};
const registerUserSellerService = async (userData) => {
    const validUserData = {
        email:userData.email,
        name:userData.firstName,
        surname:userData.lastName,
        bank_data:userData.bankData,
        cif:userData.cif,
        password:userData.password,
        birth_date:userData.birth_date
    }
    try {
        const response = await axiosInstance.post('/sellers', validUserData);
        console.log('Registro de vendedor exitoso', response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al registrar al usuario:', error);
        throw error;
    }
};
const loginUserService = async (userData) => {
    const params = new URLSearchParams();
    params.append('username', userData.email);
    params.append('password', userData.password);
    try {
        console.log('Intentando loguear: ', userData);
        const response = await axiosInstance.post('/login/access-token', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        localStorage.setItem('accessToken', response.data.access_token);
        const myData = await myInfoService();
        localStorage.setItem('type', myData.type);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al loguear el usuario:', error.response ? error.response.data : error);
        throw error;
    }
}
const myInfoService = async () => {
    try {
        const response = await axiosInstance.get('/users/me/');
        return response.data
    } catch (error) {
        console.error('Hubo un error obtener la informacion del usuario: ', error.response ? error.response.data : error);
        throw error;
    }
}
export {registerUserSellerService, registerUserBuyerService, loginUserService, myInfoService};