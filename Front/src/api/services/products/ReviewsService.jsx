import axiosInstance from 'axios';

export const getProductReviews = async (seller_product_id) => {
    try {
        const response = await axiosInstance.get(`/seller_products/${seller_product_id}/reviews`);
        return response.data;
    } catch (error) {
        throw error;
    }
};
