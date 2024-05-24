import axiosInstance from '../AxiosInstance';

const createOrder = async (orderData) => {
    try {
        const response = await axiosInstance.post('/orders/me', orderData);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener los productos', error.response ? error.response.data : error);
        throw error;
    }
};
const getOrders = async () => {
    try {
        const response = await axiosInstance.get('/orders/me');
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener los productos', error.response ? error.response.data : error);
        throw error;
    }
};

export { createOrder, getOrders };