import axios from '../AxiosInstance'; 
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
    };
    try {
        console.log("buyer: ", validBuyerData)
        const response = await axios.post('http://127.0.0.1:8000/buyers', validBuyerData);
        console.log('Registro de comprador exitoso', response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al registrar al comprador:', error.response ? error.response.data : error);
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
export {registerUserSellerService, registerUserBuyerService};