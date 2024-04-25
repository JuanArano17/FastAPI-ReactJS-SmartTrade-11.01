import axiosInstance from '../AxiosInstance';
import { createProductFromApiResponse } from "../../../models/ProductModel"
import { createProductSellerFromApiResponse } from "../../../models/ProductSellerModel"

const getAllProducts = async () => {
    try {
        console.log("Intentando conseguir todos los productos...");
        const response = await axiosInstance.get('products/');
        console.log("respuesta api", response);
        const formattedProducts = response.data.map(product => createProductFromApiResponse(product));
        console.log("productos formateados", formattedProducts);
        return formattedProducts;
    } catch (error) {
        console.error('Hubo un error al obtener los productos', error.response ? error.response.data : error);
        throw error;
    }
};
const getAllProductsSeller = async () => {
    try {
        console.log("Intentando conseguir todos los productos de los vendedores...")
        const response = await axiosInstance.get('seller_products/');
        console.log("respuesta api", response);
        const formattedProducts = response.data.map(product => createProductSellerFromApiResponse(product));
        console.log("productos formateados", formattedProducts);
        return formattedProducts;
    } catch (error) {
        console.error('Hubo un error al obtener productos', error.response ? error.response.data : error);
        throw error;
    }
}
const getProductById = async (product_id) => {
    try {
        console.log("Intentando conseguir el producto...")
        const response = await axiosInstance.get(`products/${product_id}`);
        console.log("producto conseguido correctamente", response)
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener el producto', error.response ? error.response.data : error);
    }
}
const getProductSellerById = async (product_id) => {
    try {
        console.log("Intentando conseguir el producto...")
        const response = await axiosInstance.get(`/seller-products/${product_id}/`);
        console.log("producto conseguido correctamente", response)
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener el producto', error.response ? error.response.data : error);
    }
}
export { getProductById,getAllProducts, getAllProductsSeller, getProductSellerById }