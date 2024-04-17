import axiosInstance from '../AxiosInstance'; 
import {createProductFromApiResponse} from "../../../models/ProductModel"
const getAllProducts = async () => {
    try {
        console.log("Intentando conseguir todos los productos...");
        const response = await axiosInstance.get('/products');
        console.log("respuestaapi", response);
        const products = response.data.map(product => createProductFromApiResponse(product));
        return products;
    } catch (error) {
        console.error('Hubo un error al obtener productos', error.response ? error.response.data : error);
        throw error;
    }
};
const getAllProductsSeller = async () => {
    try {
        console.log("Intentando conseguir todos los productos de los vendedores...")
        const response = await axiosInstance.get('/seller-products');
        console.log("respuestaapi", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener productos', error.response ? error.response.data : error);
        throw error;
    }
}
const getAllProductsSellerComplete = async () => {
    try {
        console.log("Intentando conseguir todos los productos de los vendedores completos...")
        const response = await axiosInstance.get('/seller-products/all');
        console.log("respuestaapi", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener productos', error.response ? error.response.data : error);
        throw error;
    }
}
export {getAllProducts, getAllProductsSeller, getAllProductsSellerComplete}