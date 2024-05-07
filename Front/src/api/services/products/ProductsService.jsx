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
const getProductSellerById = async (product_id) => {
    try {
        console.log(`Intentando conseguir el producto con id: ${product_id}...`);
        const response = await axiosInstance.get(`/seller_products/${product_id}`);
        console.log("producto conseguido correctamente", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener el producto', error.response ? error.response.data : error);
    }
}
const editSellerProductById = async (product) => {
    const formatedProduct = {
        quantity: product.quantity,
        price: product.price,
        shipping_costs: product.shipping_costs,
        state: product.state,
        justification: product.justification,
        eco_points: product.eco_points,
        age_restricted: product.age_restricted
    };
    try {
        console.log(`Intentando editar el producto con id: ${product.id}...`);
        const response = await axiosInstance.put(`/seller_products/${product.id}`);
        console.log("producto editado correctamente", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al editar el producto', error.response ? error.response.data : error);
    }
}
const createSellerProduct = async (product, sellerId) => {
    try {
        console.log("Intentando crear un nuevo producto de vendedor...");
        const response = await axiosInstance.post(`/seller_products?seller_id=${sellerId}`, {
            quantity: parseInt(product.quantity, 10) || 0,
            price: parseFloat(product.price) || 0.0,
            shipping_costs: parseFloat(product.shipping_costs) || 0.0,
            sizes: product.sizes || [],
            id_product: parseInt(product.id_product, 10) || 0
        });
        console.log("Producto creado correctamente", response.data);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al crear el producto', error.response ? error.response.data : error);
        throw error;
    }
};

const getAllSellerProducts = async () => {
    try {
        console.log("Intentando conseguir todos los productos...");
        const response = await axiosInstance.get('/seller_products/me/');
        console.log("respuesta api", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener los seller productos', error.response ? error.response.data : error);
        throw error;
    }
};
const deleteSellerProduct = async (seller_product_id) => {
    try {
  
      const sellerproductResponse = await axiosInstance.delete(`/seller_products/${seller_product_id}`);
      console.log('Se ha eliminado el seller product con éxito:', sellerproductResponse.data);
      return sellerproductResponse.data;
    } catch (error) {
      console.error('Error al eliminar seller product:', error);
      throw error;
    }
  };


export { getAllProducts, getProductById, getAllProductsSeller, getProductSellerById, editSellerProductById, createSellerProduct, getAllSellerProducts, deleteSellerProduct}