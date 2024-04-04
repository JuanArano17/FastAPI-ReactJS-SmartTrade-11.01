import axios from '../AxiosInstance'; 
const registerCardService = async (cardInfo) => {
    try {
        const response = await axios.post('/credit-card/register', cardInfo);
        console.log('Registro de tarjeta exitoso:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al registrar la tarjeta:', error);
        throw error;
    }
};
export default registerCardService;