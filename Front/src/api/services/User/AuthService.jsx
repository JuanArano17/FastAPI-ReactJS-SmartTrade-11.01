import axios from '../AxiosInstance'; 
const registerUserBuyerService = async (userData) => {
    try {
        const response = await axios.post('auth/register', userData);
        console.log('Registro exitoso', response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al registrar al usuario:', error);
        throw error;
    }
};
const registerUserSellerService = async (userData) => {
    try {
        const response = await axios.post('auth/register', userData);
        console.log('Registro exitoso', response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al registrar al usuario:', error);
        throw error;
    }
};
export default {registerUserSellerService, registerUserBuyerService};