import axiosInstance from '../AxiosInstance';
const deleteCartItem = async (item_id) => {
  const validbuyerid = {
    seller_product_id: item_id
  }
  try {
    const response = await axiosInstance.delete(`/shopping_cart/me/${validbuyerid.seller_product_id}`, validbuyerid.seller_product_id);
    console.log('Se ha eliminado el item con éxito:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error al eliminar el item:', error);
    throw error;
  }
};
const getCartItems = async () => {
  try {
    const response = await axiosInstance.get('/shopping_cart/me');
    console.log('Los productos del carrito son:', response);
    return response.data;
  } catch (error) {
    console.error('Error al recuperar productos del carrito:', error);
    throw error;
  }
};
const getSellerProduct = async (productId) => {
  try {
    const response = await axiosInstance.get(productId);
    console.log('Los productos del carrito son:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error al obtener información del productoAAAAAA:', error);
    throw error;
  }
};
const addCartItem = async (sellerProductId, quantity, id_size = null) => {
  const requestBody = {
      id_seller_product: sellerProductId,
      quantity: quantity
  };
  let url = '/shopping_cart/me/';
  if (id_size) {
      url += `?id_size=${id_size}`; 
  }
  try {
      const response = await axiosInstance.post(url, requestBody);
      return response.data;
  } catch (error) {
      console.error('Error al añadir producto al carrito', error);
      throw error;
  }
};

const updateCartItemQuantity = async (id_cart_item, quantity) => {
  const requestBody = {
    quantity: quantity,
  };

  try {
    const response = await axiosInstance.put(`/shopping_cart/me/${id_cart_item}`, requestBody);
    return response.data;
  } catch (error) {
    console.error('Error al actualizar la cantidad del producto en el carrito:', error);
    throw error;
  }
};

const updateSellerProductStock = async (sellerProductId, updateData) => {
  try {
      const response = await axiosInstance.put(`/seller_products/${sellerProductId}`, updateData);
      return response.data;
  } catch (error) {
      console.error('Error al actualizar el stock del producto:', error.response ? error.response.data : error);
      throw error;
  }
};


const clearCart = async () => {
  try {
      const response = await axiosInstance.delete('/shopping_cart/me/');
      return response.data;
  } catch (error) {
      console.error('Error al vaciar el carrito:', error.response ? error.response.data : error);
      throw error;
  }
};




export { clearCart,updateSellerProductStock, updateCartItemQuantity, addCartItem, deleteCartItem, getCartItems };