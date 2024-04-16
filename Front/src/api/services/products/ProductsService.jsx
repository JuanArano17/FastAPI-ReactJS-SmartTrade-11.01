import axiosInstance from '../AxiosInstance'; 
const getAllProducts = async () => {
    try {
        console.log("Intentando conseguir todos los productos...")
        response = axiosInstance.get('/products');
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener productos', error.response ? error.response.data : error);
        throw error;
    }
}
export {getAllProducts}