import React from 'react';
import { Button } from '@mui/material';

const ImageUpload = ({ images, setImages, imagePreviews, setImagePreviews }) => {
  const handleImageChange = (event) => {
    const files = Array.from(event.target.files);
    const newFiles = files.filter(file => !images.some(img => img.name === file.name && img.size === file.size));

    const newImageFiles = [...images, ...newFiles];
    const newImagePreviews = [...imagePreviews, ...newFiles.map(file => URL.createObjectURL(file))];

    setImages(newImageFiles);
    setImagePreviews(newImagePreviews);
    
  };

  const handleRemoveImage = (index) => {
    const newImages = images.filter((_, i) => i !== index);
    const newPreviews = imagePreviews.filter((_, i) => i !== index);
    setImagePreviews(newPreviews);
    setImages(newImages);
  };

  return (
    <>
      <Button
        variant="contained"
        component="label"
        fullWidth
      >
        Upload Images
        <input
          type="file"
          hidden
          multiple
          onChange={handleImageChange}
        />
      </Button>
      <div style={{ marginTop: 20, position: 'relative' }}>
        {imagePreviews.map((src, index) => (
          <div key={index} style={{ display: 'inline-block', position: 'relative', marginRight: 10 }}>
            <img src={src} alt="preview" style={{ width: 100, height: 100 }} />
            <Button
              onClick={() => handleRemoveImage(index)}
              style={{
                position: 'absolute',
                top: 0,
                right: 0,
                minWidth: '30px',
                height: '30px',
                fontSize: '16px',
                color: '#fff',
                backgroundColor: 'rgba(255,0,0,0.7)',
                border: 'none',
                cursor: 'pointer'
              }}>
              X
            </Button>
          </div>
        ))}
      </div>
    </>
  );
};

export default ImageUpload;
