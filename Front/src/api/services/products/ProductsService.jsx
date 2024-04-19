import axiosInstance from '../AxiosInstance';
import { createProductFromApiResponse, getDefaultProductModel } from "../../../models/ProductModel"

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
                    sellerId: seller.id_seller, // Cambio de nombre para claridad
                    id_seller_product: seller.id, // Cambio de nombre para aclarar que es el ID del producto del vendedor
                    stock: seller.quantity, // Usar `quantity` para el stock
                    category: product.category,
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
const getWishItems = async () => {
    try {
        const response = await axiosInstance.get('/wish_list/me');
        console.log('Los productos del wishlist son:', response);
        return response.data;
    } catch (error) {
        console.error('Error al recuperar productos del wishlist:', error);
        throw error;
    }
};
const addToWishList = async (id_seller) => {
    const requestBody = {
        id_seller_product: id_seller,
    };
    try {
        const response = await axiosInstance.post('/wish_list/me', requestBody);
        console.log('Se agrego un elemento con exito', response);
        return response.data;
    } catch (error) {
        console.error('Error al agregar elemento al wishlist:', error);
        throw error;
    }
};
const deleteFromWishList = async (id_seller) => {
    const requestBody = {
        id_seller_product: id_seller,
    };
    try {
        const response = await axiosInstance.delete(`/wish_list/me/${requestBody.id_seller_product}`, requestBody);
        console.log('Se elimino un elemento con exito', response);
        return response.data;
    } catch (error) {
        console.error('Error al eliminar elemento del wishlist:', error);
        throw error;
    }
};
export {getProduct,getAllProducts, getAllProductsSeller, getAllProductsSellerComplete, getWishItems, addToWishList, deleteFromWishList}