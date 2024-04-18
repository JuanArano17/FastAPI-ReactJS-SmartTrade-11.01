import axiosInstance from '../AxiosInstance'; 
const deleteItemService = async (user_id,item_id) => {
    const validbuyerid = { 
        buyer_id:user_id,
        seller_product_id:item_id
    }
    try {
        const response = await axiosInstance.delete(`/buyers/${validbuyerid.buyer_id}/shopping_cart/${validbuyerid.seller_product_id}`, validbuyerid);
        console.log('Se ha eliminado el item con éxito:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al eliminar el item:', error);
        throw error;
    }
};
const getCartItems = async (user_id) => {
    const validbuyerid = { 
        buyer_id:user_id,
    }
    try {
        const response = await axiosInstance.get(`/buyers/${validbuyerid.buyer_id}/shopping_cart/`, validbuyerid);
        console.log('Los productos del carrito son:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al recuperar productos del carrito:', error);
        throw error;
    }
};
const getSellerProduct = async (productId) => {
    try {
        const response = await getSellerProduct(productId);
        console.log('Los productos del carrito son:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener información del producto:', error);
        throw error;
    }
};


export default {getSellerProduct, deleteItemService,getCartItems};