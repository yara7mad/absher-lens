document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("imageUpload");
    const resultDiv = document.getElementById("result");

    fileInput.addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        resultDiv.innerHTML = `<div class="loader"></div><p>جاري تحليل الذكاء الاصطناعي...</p>`;

        const formData = new FormData();
        formData.append("image", file);

        try {
            const res = await fetch("/analyze", { method: "POST", body: formData });
            const data = await res.json();
            const a = data.analysis || data;

            // SAVE DATA for the next page
            localStorage.setItem('absherAnalysis', JSON.stringify(a));

            resultDiv.innerHTML = `
                <div class="result-box">
                    <h3 style="color:var(--primary)">${a.type}</h3>
                    <p><strong>المطلوب:</strong> ${a.required_action}</p>
                    <a href="/action" class="btn">عرض خطة التنفيذ</a>
                </div>
            `;
        } catch (err) {
            resultDiv.innerHTML = "<p>حدث خطأ، يرجى المحاولة مرة أخرى</p>";
        }
    });
});