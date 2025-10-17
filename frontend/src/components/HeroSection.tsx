import { EyeFollower } from "./EyeFollower";
import { Button } from "./ui/button";
import { ArrowDown } from "lucide-react";

export const HeroSection = () => {
  const scrollToDemo = () => {
    document.getElementById("demo")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section id="home" className="min-h-screen bg-gradient-hero relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-20 left-10 w-32 h-32 bg-primary/5 rounded-full blur-3xl" />
      <div className="absolute bottom-20 right-10 w-40 h-40 bg-accent/5 rounded-full blur-3xl" />

      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
          {/* Eye Collection */}
          <div className="relative mb-12 w-full max-w-4xl">
            {/* Smaller eyes around the main eye */}
            <div className="absolute top-0 left-[10%] animate-float">
              <EyeFollower size="small" />
            </div>
            <div className="absolute top-10 right-[15%] animate-float" style={{ animationDelay: "0.5s" }}>
              <EyeFollower size="small" />
            </div>
            <div className="absolute bottom-20 left-[20%] animate-float" style={{ animationDelay: "1s" }}>
              <EyeFollower size="medium" />
            </div>
            <div className="absolute bottom-10 right-[25%] animate-float" style={{ animationDelay: "1.5s" }}>
              <EyeFollower size="medium" />
            </div>

            {/* Main large eye */}
            <div className="flex justify-center">
              <EyeFollower size="large" className="shadow-2xl" />
            </div>
          </div>

          {/* Hero Content */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-primary bg-clip-text text-transparent">
            Cognivasc  - Ứng dụng AI    chẩn đoán bệnh thiếu máu
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl">
            Phân tích kết mạc mắt bằng công nghệ AI tiên tiến để phát hiện thiếu máu một cách nhanh chóng và chính xác.
          </p>
          <Button 
            onClick={scrollToDemo}
            size="lg"
            className="bg-gradient-primary text-primary-foreground hover:opacity-90 transition-all hover:scale-105 shadow-medium text-lg px-8 py-6"
          >
            Thử AI Demo ngay
            <ArrowDown className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* About Section */}
      <div className="container mx-auto px-4 pb-20">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-card rounded-2xl p-8 md:p-12 shadow-soft backdrop-blur">
            <h2 className="text-3xl md:text-4xl font-bold mb-6 text-center text-primary">
              Cognivasc Là Gì?
            </h2>
            <div className="space-y-4 text-muted-foreground text-lg leading-relaxed">
              <p>
                Thiếu máu là tình trạng máu của bạn không có đủ hồng cầu khỏe mạnh để vận chuyển lượng oxy
                cần thiết đến các mô trong cơ thể. Bệnh lý này ảnh hưởng đến hàng triệu người trên toàn thế
                giới và có thể dẫn đến mệt mỏi, suy nhược, cũng như các biến chứng sức khỏe nghiêm trọng nếu
                không được điều trị kịp thời.
              </p>
              <p>
                Công cụ AI tiên tiến của chúng tôi phân tích kết mạc mắt (bề mặt trong của mí mắt)
                để nhanh chóng phát hiện các dấu hiệu thiếu máu. Màu sắc và hình thái của kết mạc
                phản ánh mức oxy trong máu, mang đến một chỉ số chẩn đoán cực kỳ giá trị.
              </p>
              <p className="text-primary font-semibold">
                Với sự kết hợp giữa chuyên môn y tế và công nghệ trí tuệ nhân tạo hiện đại,
                chúng tôi mang đến giải pháp sàng lọc ban đầu nhanh chóng, không xâm lấn và
                chính xác, giúp bạn chủ động chăm sóc sức khỏe từ sớm.
              </p>
              <p className="text-sm text-muted-foreground/80 italic mt-6 border-l-4 border-accent pl-4">
                Lưu ý: Đây là công cụ nghiên cứu và không thay thế cho chẩn đoán y tế chuyên nghiệp.
                Luôn tham khảo ý kiến bác sĩ hoặc chuyên gia y tế để được đánh giá và điều trị chính xác.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
