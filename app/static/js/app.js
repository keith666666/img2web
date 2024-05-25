const MAX_FILE_SIZE = 4 * 1024 * 1024; // 4 MB
const MAX_FILE_SIZE_MB = MAX_FILE_SIZE / (1024 * 1024); // Convert to MB

document.addEventListener("alpine:init", () => {
  Alpine.data("updateAndGenerate", () => ({
    isUploading: false,
    pageUrl: "",

    async uploadImage() {
      const form = document.getElementById("upload-form");
      const formData = new FormData(form);

      // Check if a file has been selected
      if (!formData.has("file") || formData.get("file").size === 0) {
        alert("Please select a file to upload.");
        return;
      }
      if (formData.get("file").size > MAX_FILE_SIZE) {
        alert(
          `File is too large. Maximum allowed size is ${MAX_FILE_SIZE_MB} MB.`
        );
        return;
      }

      try {
        this.isUploading = true;
        const response = await fetch(form.action, {
          method: "POST",
          body: formData,
        });

        const result = await response.json();

        this.isUploading = false;

        console.log("result:", result);
        // alert(result.message);
        if (result.pageUrl) {
          this.pageUrl = result.pageUrl;
        } else {
          this.pageUrl = "";
          alert(result.message);
        }
      } catch (error) {
        this.isUploading = false;
        this.pageUrl = "";
        alert("An error occurred while uploading the file.");
      }
    },
  }));
});
