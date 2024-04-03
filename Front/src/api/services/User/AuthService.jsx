import axios from '../AxiosInstance'; 
const registerUserService = async (userData) => {
    try {
        const response = await axios.post('auth/register', userData);
        console.log('Registro exitoso', response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al registrar al usuario:', error);
        throw error;
    }
};
export default registerUserService;