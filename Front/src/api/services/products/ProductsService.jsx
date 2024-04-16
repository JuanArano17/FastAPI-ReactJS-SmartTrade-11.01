import axiosInstance from '../AxiosInstance'; 
const getAllProducts = async () => {
    try {
        console.log("Intentando conseguir todos los productos...")
        const response = await axiosInstance.get('/products');
        console.log("respuestaapi", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener productos', error.response ? error.response.data : error);
        throw error;
    }
}
export {getAllProducts}