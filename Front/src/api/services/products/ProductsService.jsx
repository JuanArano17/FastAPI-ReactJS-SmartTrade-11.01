import axiosInstance from '../AxiosInstance';
import { createProductFromApiResponse } from "../../../models/ProductModel"
const getAllProducts = async () => {
    try {
        console.log("Intentando conseguir todos los productos con vendedores...");
        const response = await axiosInstance.get('/products');
        const productsWithSellers = response.data
            .filter(product => product.seller_products && product.seller_products.length > 0)
            .flatMap(product => 
                product.seller_products.map(seller => ({
                    ...createProductFromApiResponse(product),
                    price: seller.price,
                    sellerId: seller.id,
                    image: product.images.length > 0 ? product.images[0].url : null
                }))
            );
        return productsWithSellers;
    } catch (error) {
        console.error('Hubo un error al obtener los productos con vendedores', error.response ? error.response.data : error);
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
const getProduct = async (product_id) => {
    try {
        console.log("Intentando conseguir el producto...")
        const response = await axiosInstance.get(`/products/${product_id}`);
        console.log("producto conseguido correctamente", response)
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener el producto', error.response ? error.response.data : error);
    }
}
export {getProduct,getAllProducts, getAllProductsSeller, getAllProductsSellerComplete}