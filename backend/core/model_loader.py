class ModelLoader:
    _instance = None
    _vit5_model = None
    _vit5_tokenizer = None
    _embedder = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            # TODO: Khởi tạo mô hình ViT5 (AutoModelForSeq2SeqLM) và Tokenizer
            # TODO: Khởi tạo mô hình Embedding riêng biệt rải rác ngoài ViT5
        return cls._instance

    def get_vit5_components(self):
        """
        Trả về mô hình và tokenizer của ViT5 để dùng cho sinh văn bản (Seq2Seq).
        """
        # TODO: Trả về tuple (_vit5_model, _vit5_tokenizer)
        return self._vit5_model, self._vit5_tokenizer

    def get_embedder(self):
        """
        Trả về mô hình nhúng vector (Embedding). Lưu ý: ViT5 KHÔNG dùng làm embedding.
        """
        # TODO: Cài đặt hàm trả về mô hình Embedding
        return self._embedder

# Singleton instance (Chỉ khởi tạo 1 lần)
model_loader = ModelLoader()
