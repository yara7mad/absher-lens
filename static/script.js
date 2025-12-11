document.addEventListener("DOMContentLoaded", () => {

    const fileInput = document.getElementById("imageUpload");
    const resultDiv = document.getElementById("result");

    fileInput.addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("image", file);

        resultDiv.innerHTML = "<p>جاري تحليل المستند...</p>";

        try {
            const res = await fetch("/analyze", {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            console.log("SERVER:", data);

            const a = data.analysis || data; // احتياط

            resultDiv.innerHTML = `
                <div class="result-box">
                    <h3>${a.type || "إشعار"}</h3>
                    <p><strong>المطلوب:</strong> ${a.required_action || "-"}</p>
                    <p><strong>المهلة:</strong> ${a.deadline || "-"}</p>
                    <p><strong>الإجراء:</strong> ${a.next_step || "-"}</p>

                    <a href="/action" class="btn">نفّذ الإجراء الآن</a>
                </div>
            `;
        } catch (err) {
            console.error(err);
            resultDiv.innerHTML = "<p>حدث خطأ أثناء التحليل.</p>";
        }
    });

});
