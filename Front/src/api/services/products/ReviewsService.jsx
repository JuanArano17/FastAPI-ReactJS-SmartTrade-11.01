// src/api/services/products/ReviewsService.js

import axiosInstance from 'axios';

export const getProductReviews = async (sellerProductId) => {
    try {
        const response = await axiosInstance.get(`/seller_products/${sellerProductId}/reviews`);
        return response.data;
    } catch (error) {
        throw error;
    }
};
