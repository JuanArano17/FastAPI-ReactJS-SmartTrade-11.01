const tutorialData = [
    {
        title: 'Catalog Page',
        description: 'The catalog page is the heart of our application, where users can browse all available products. Here, users can see a wide range of products, organized in a visually appealing grid. Each product displays key information such as name, brief description, EcoPoints, and price. Additionally, users can filter products by category and price range using the controls at the top of the page.',
        image: process.env.PUBLIC_URL + '/images/tutorial/Catalog.png'
    },
    {
        title: 'Filter Products',
        description: 'On the catalog page, users can apply filters to refine their search. The category filter allows selecting different types of products, such as electronics, clothing, books, etc. The price range slider allows users to set a specific price range to find products that fit their budget. There is also a button to clear all applied filters and reset the search.',
        image: process.env.PUBLIC_URL + '/images/tutorial/FilterProducts.png'
    },
    {
        title: 'Home Page',
        description: 'The home page welcomes users with an overview of our application. Here, users can get a quick glimpse of what Smart Trade offers, including its commitment to green sales. The page features a clean and attractive design with a welcome message and a representative image highlighting our mission.',
        image: process.env.PUBLIC_URL + '/images/tutorial/HomePage.png'
    },
    {
        title: 'Login Page',
        description: 'The login page allows users to access their personal accounts on Smart Trade. Users need to enter their email and password to authenticate. A link to recover the password is also provided in case users forget it. This page is essential to protect user information and offer a personalized experience.',
        image: process.env.PUBLIC_URL + '/images/tutorial/Login.png'
    },
    {
        title: 'Login General Page',
        description: 'The general login page allows users to register or log in to Smart Trade. From here, users can choose to sign up as new users or log in if they already have an account. This entry point is crucial to ensure that only authorized users can access the advanced functionalities of the application.',
        image: process.env.PUBLIC_URL + '/images/tutorial/LoginGeneral.png'
    },
    {
        title: 'Products Panel Seller',
        description: 'The products panel for sellers allows users who sell products on Smart Trade to manage their inventory. On this page, sellers can see a list of all their products, along with details such as available quantity, price, shipping costs, and publication status. They can also perform actions such as editing or deleting products directly from this interface.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProductsPanelSeller.png'
    },
    {
        title: 'Add Product Panel',
        description: 'The add product form allows sellers to add new products to their catalog. Sellers need to provide details such as product name, category, description, specification sheet, price, shipping costs, and available quantity. They can also upload product images to attract buyers. This form ensures that products are presented comprehensively and attractively in the store.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProductsPanelSellerAdd.png'
    },
    {
        title: 'Profile Page',
        description: 'The user profile page displays personal information and allows editing. Users can view details such as their first name, last name, email, tax ID, and bank details. This page is essential for users to keep their information updated and manage their personal data securely.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProfilePageSeller.png'
    },
    {
        title: 'Profile Page - Buyer Cards',
        description: 'In the cards section of the profile page, users can manage their payment methods. They can add, edit, or delete credit and debit cards to facilitate their purchases on Smart Trade. This functionality ensures that users always have an updated and valid payment method.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProfilePageBuyerCards.png'
    },
    {
        title: 'Profile Page - Buyer Personal Info',
        description: 'The personal information section of the profile page allows users to view and update their personal details. This includes details such as first name, last name, email address, tax ID, date of birth, and billing address. Keeping this information updated is crucial for effective communication and a personalized experience.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProgilePageBuyerPersonalInfo.png'
    },
    {
        title: 'Profile Page - Buyer Shipping Address',
        description: 'In the shipping address section of the profile page, users can manage their shipping addresses. They can add new addresses, edit existing ones, or delete those no longer needed. This ensures that purchased products are shipped to the correct address.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ProgilePageBuyerShippingAddress.png'
    },
    {
        title: 'Register Buyer',
        description: 'The buyer registration page allows new users to create an account on Smart Trade. Users need to provide basic information such as first name, last name, email address, tax ID, and a password. They also have the option to add credit card information to facilitate future purchases.',
        image: process.env.PUBLIC_URL + '/images/tutorial/RegisterBuyer.png'
    },
    {
        title: 'Register Seller',
        description: 'The seller registration page allows users to sign up as sellers on Smart Trade. They need to provide basic information such as first name, last name, email address, and a password, in addition to additional details such as the tax ID and bank details to receive payments.',
        image: process.env.PUBLIC_URL + '/images/tutorial/RegisterSeller.png'
    },
    {
        title: 'Search Bar',
        description: 'The search bar allows users to search for specific products on Smart Trade. By entering keywords into the search field, users can quickly find the products they want. This functionality is essential to improve user experience and facilitate navigation in the store.',
        image: process.env.PUBLIC_URL + '/images/tutorial/SearchBar.png'
    },
    {
        title: 'Shopping Cart',
        description: 'The shopping cart allows users to view and manage the products they want to buy. They can adjust quantities, remove products, and see the accumulated total. This functionality is crucial to provide a convenient and efficient shopping experience.',
        image: process.env.PUBLIC_URL + '/images/tutorial/ShoppingCart.png'
    },
    {
        title: 'Wish List',
        description: 'The wish list allows users to save products they are interested in for later purchase. Users can add or remove products from their wish list and see current prices. This functionality helps users remember products of interest and plan their future purchases.',
        image: process.env.PUBLIC_URL + '/images/tutorial/WishList.png'
    }
];

export default tutorialData;
