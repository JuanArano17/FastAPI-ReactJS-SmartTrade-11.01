const tutorialData = [
    {
        title: 'Catalog Page',
        description: 'La página del catálogo es el corazón de nuestra aplicación, donde los usuarios pueden navegar por todos los productos disponibles. Aquí, los usuarios pueden ver una amplia gama de productos, organizados en una cuadrícula visualmente atractiva. Cada producto muestra información clave como el nombre, la descripción breve, los EcoPoints y el precio. Además, los usuarios pueden filtrar los productos por categoría y rango de precios utilizando los controles en la parte superior de la página.',
        image: process.env.PUBLIC_URL + '/images/tutorial/Catalog.png'
    },
    {
        title: 'Filter Products',
        description: 'En la página del catálogo, los usuarios pueden aplicar filtros para refinar su búsqueda. El filtro de categoría permite seleccionar diferentes tipos de productos, como electrónicos, ropa, libros, etc. El control deslizante de rango de precios permite a los usuarios establecer un rango de precios específico para encontrar productos que se ajusten a su presupuesto. También hay un botón para limpiar todos los filtros aplicados y reiniciar la búsqueda.',
        image: process.env.PUBLIC_URL + '/images/tutorial/FilterProducts.png'
    },
    {
        title: 'Home Page',
        description: 'La página de inicio da la bienvenida a los usuarios con una presentación general de nuestra aplicación. Aquí, los usuarios pueden obtener una visión rápida de lo que ofrece Smart Trade, incluyendo su compromiso con las ventas ecológicas. La página presenta un diseño limpio y atractivo con un mensaje de bienvenida y una imagen representativa que resalta nuestra misión.',
        image: process.env.PUBLIC_URL + '/images/tutorial/HomePage.png'
    },
    {
        title: 'Login Page',
        description: 'La página de inicio de sesión permite a los usuarios acceder a sus cuentas personales en Smart Trade. Los usuarios deben ingresar su correo electrónico y contraseña para autenticarse. También se proporciona un enlace para recuperar la contraseña en caso de que los usuarios la olviden. Esta página es esencial para proteger la información del usuario y ofrecer una experiencia personalizada.',
        image: process.env.PUBLIC_URL + '/images/tutorial/Login.png'
    },
    {
        title: 'Login General Page',
        description: 'La página de inicio de sesión general permite a los usuarios registrarse o iniciar sesión en Smart Trade. Desde aquí, los usuarios pueden elegir entre registrarse como nuevos usuarios o iniciar sesión si ya tienen una cuenta. Este punto de entrada es crucial para garantizar que solo los usuarios autorizados puedan acceder a las funcionalidades avanzadas de la aplicación.',
        image: process.env.PUBLIC_URL + '/images/tutorial/LoginGeneral.png'
    },
    {
        title: 'Products Panel Seller',
        description: 'El panel de productos para vendedores permite a los usuarios que venden productos en Smart Trade gestionar su inventario. En esta página, los vendedores pueden ver una lista de todos sus productos, junto con detalles como la cantidad disponible, el precio, los costos de envío y el estado de publicación. También pueden realizar acciones como editar o eliminar productos directamente desde esta interfaz.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProductsPanelSeller.png'
    },
    {
        title: 'Add Product Panel',
        description: 'El formulario para añadir productos permite a los vendedores agregar nuevos productos a su catálogo. Los vendedores deben proporcionar detalles como el nombre del producto, la categoría, la descripción, la hoja de especificaciones, el precio, los costos de envío y la cantidad disponible. También pueden subir imágenes del producto para atraer a los compradores. Este formulario asegura que los productos se presenten de manera completa y atractiva en la tienda.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProductsPanelSellerAdd.png'
    },
    {
        title: 'Profile Page',
        description: 'La página de perfil del usuario muestra información personal y permite editarla. Los usuarios pueden ver detalles como su nombre, apellido, correo electrónico, CIF y datos bancarios. Esta página es esencial para que los usuarios mantengan su información actualizada y gestionen sus datos personales de manera segura.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProfilePageSeller.png'
    },
    {
        title: 'Profile Page - Buyer Cards',
        description: 'En la sección de tarjetas de la página de perfil, los usuarios pueden gestionar sus métodos de pago. Pueden añadir, editar o eliminar tarjetas de crédito y débito para facilitar sus compras en Smart Trade. Esta funcionalidad asegura que los usuarios tengan siempre un método de pago actualizado y válido.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProfilePageBuyerCards.png'
    },
    {
        title: 'Profile Page - Buyer Personal Info',
        description: 'La sección de información personal de la página de perfil permite a los usuarios ver y actualizar sus datos personales. Esto incluye detalles como nombre, apellido, dirección de correo electrónico, DNI, fecha de nacimiento y dirección de facturación. Mantener esta información actualizada es crucial para una comunicación efectiva y una experiencia personalizada.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProgilePageBuyerPersonalInfo.png'
    },
    {
        title: 'Profile Page - Buyer Shipping Address',
        description: 'En la sección de direcciones de envío de la página de perfil, los usuarios pueden gestionar sus direcciones de envío. Pueden añadir nuevas direcciones, editar las existentes o eliminar las que ya no necesiten. Esto garantiza que los productos comprados se envíen a la dirección correcta.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProgilePageBuyerShippingAddress.png'
    },
    {
        title: 'Register Buyer',
        description: 'La página de registro de compradores permite a los nuevos usuarios crear una cuenta en Smart Trade. Los usuarios deben proporcionar información básica como nombre, apellido, dirección de correo electrónico, DNI y una contraseña. También tienen la opción de añadir información de la tarjeta de crédito para facilitar futuras compras.',
        image: process.env.PUBLIC_URL + '/images/tutorial/RegisterBuyer.png'
    },
    {
        title: 'Register Seller',
        description: 'La página de registro de vendedores permite a los usuarios registrarse como vendedores en Smart Trade. Deben proporcionar información básica como nombre, apellido, dirección de correo electrónico y una contraseña, además de detalles adicionales como el CIF y los datos bancarios para recibir pagos.',
        image: process.env.PUBLIC_URL + '/images/tutorial/RegisterSeller.png'
    },
    {
        title: 'Search Bar',
        description: 'La barra de búsqueda permite a los usuarios buscar productos específicos en Smart Trade. Al ingresar palabras clave en el campo de búsqueda, los usuarios pueden encontrar rápidamente los productos que desean. Esta funcionalidad es esencial para mejorar la experiencia de usuario y facilitar la navegación en la tienda.',
        image: process.env.PUBLIC_URL + '/images/tutorial/SearchBar.png'
    },
    {
        title: 'Shopping Cart',
        description: 'El carrito de compras permite a los usuarios ver y gestionar los productos que desean comprar. Pueden ajustar las cantidades, eliminar productos y ver el total acumulado. Esta funcionalidad es crucial para proporcionar una experiencia de compra conveniente y eficiente.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ShoppingCart.png'
    },
    {
        title: 'Wish List',
        description: 'La lista de deseos permite a los usuarios guardar productos que les interesan para comprarlos más tarde. Los usuarios pueden añadir o eliminar productos de su lista de deseos y ver los precios actuales. Esta funcionalidad ayuda a los usuarios a recordar productos de interés y planificar sus compras futuras.',
        image: process.env.PUBLIC_URL + '/images/tutorial/WishList.png'
    }
];

export default tutorialData;
