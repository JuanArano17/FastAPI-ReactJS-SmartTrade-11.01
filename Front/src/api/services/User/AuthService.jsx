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
        const response = await axios.post('/buyers', validBuyerData);
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
    }
    try {
        const response = await axios.post('/sellers', validUserData);
        console.log('Registro de vendedor exitoso', response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al registrar al usuario:', error);
        throw error;
    }
};
export {registerUserSellerService, registerUserBuyerService};