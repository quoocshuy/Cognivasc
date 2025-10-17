import { useState } from "react";
import { Mail, MessageSquare, User } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { Card } from "./ui/card";
import { toast } from "sonner";

export const ContactSection = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.message) {
      toast.error("Vui lòng điền đầy đủ tất cả các thông tin.");
      return;
    }

    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      toast.success("Gửi tin nhắn thành công! Chúng tôi sẽ sớm liên hệ lại với bạn.");
      setFormData({ name: "", email: "", message: "" });
      setIsSubmitting(false);
    }, 1000);
  };

  return (
    <section id="contact" className="min-h-screen bg-gradient-hero py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 text-primary">
            Liên Hệ
          </h2>
          <p className="text-center text-muted-foreground mb-12 text-lg">
            Bạn có thắc mắc hoặc góp ý? Chúng tôi rất mong nhận được phản hồi từ bạn!
          </p>

          <Card className="p-8 md:p-12 shadow-medium bg-gradient-card">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name */}
              <div className="space-y-2">
                <label htmlFor="name" className="text-sm font-semibold flex items-center text-foreground">
                  <User className="w-4 h-4 mr-2 text-primary" />
                  Họ Tên
                </label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Họ tên của bạn"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="bg-background/50 border-border focus:border-primary"
                />
              </div>

              {/* Email */}
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-semibold flex items-center text-foreground">
                  <Mail className="w-4 h-4 mr-2 text-primary" />
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your.email@example.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className="bg-background/50 border-border focus:border-primary"
                />
              </div>

              {/* Message */}
              <div className="space-y-2">
                <label htmlFor="message" className="text-sm font-semibold flex items-center text-foreground">
                  <MessageSquare className="w-4 h-4 mr-2 text-primary" />
                  Tin nhắn
                </label>
                <Textarea
                  id="message"
                  placeholder="Hãy chia sẻ ý kiến hoặc góp ý của bạn với chúng tôi..."
                  value={formData.message}
                  onChange={(e) =>
                    setFormData({ ...formData, message: e.target.value })
                  }
                  className="bg-background/50 border-border focus:border-primary min-h-[150px] resize-none"
                />
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-gradient-primary text-primary-foreground hover:opacity-90 transition-all hover:scale-105 text-lg py-6"
              >
                {isSubmitting ? "Đang gửi..." : "Gửi tin nhắn"}
              </Button>
            </form>
          </Card>

          {/* Additional Contact Info */}
          <div className="mt-12 text-center space-y-4">
            <p className="text-muted-foreground">
              Đối với các thắc mắc y tế khẩn cấp, vui lòng liên hệ trực tiếp với bác sĩ hoặc cơ sở y tế của bạn.
            </p>
            <div className="flex justify-center space-x-6 text-sm text-muted-foreground">
              <a href="mailto:support@anemiadetection.ai" className="hover:text-primary transition-colors">
                nguyenngocquochuy0609@gmail.com
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
