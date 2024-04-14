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
export default deleteItemService;