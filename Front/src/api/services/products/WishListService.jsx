import axiosInstance from '../AxiosInstance';
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
export { getWishItems, addToWishList, deleteFromWishList }