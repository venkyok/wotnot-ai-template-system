<template>
  <div class="bg-container">
    <div class="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">
      <h2
        class="text-2xl sm:text-2xl font-semibold text-center text-gray-800 mb-4"
      >
        Get started with <span class="logo">WotNot</span>
      </h2>

      <hr class="my-3 border-gray-300" />

      <div class="space-y-4">
        <div class="w-full">
          <label for="username" class="block text-sm font-medium text-gray-700"
            >Business Name</label
          >
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder=""
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>

        <div class="w-full">
          <label for="email" class="block text-sm font-medium text-gray-700"
            >Business Email Address</label
          >
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder=""
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>

        <div class="w-full">
          <label for="password" class="block text-sm font-medium text-gray-700"
            >Password</label
          >
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Set Password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
          <div
            class="h-2 mt-2 rounded transition-all duration-300"
            :style="{ width: strengthWidth, backgroundColor: strengthColor }"
          ></div>
          <p class="text-sm mt-1 font-medium" :style="{ color: strengthColor }">
            {{ strengthLabel }}
          </p>
        </div>

        <div class="mt-4 text-sm text-center">
          <p class="mb-2 text-sm">
            By signing up you agree to the
            <router-link
              to="/terms-and-privacy#terms-and-conditions"
              class="text-[#075e54] font-semibold"
              >Terms</router-link
            >
            and
            <router-link
              to="/terms-and-privacy#privacy-policy"
              class="text-[#075e54] font-semibold"
              >Privacy Policy</router-link
            >
          </p>
        </div>
      </div>

      <div
        ref="turnstileContainer"
        class="turnstile-container"
      ></div>

      <div class="flex flex-col items-center">
        <button
          class="w-full bg-gradient-to-r from-[#075e54] via-[#089678] to-[#075e54] text-white px-6 py-3 rounded-lg shadow-lg font-medium flex items-center justify-center hover:from-[#078478] hover:via-[#08b496] hover:to-[#078478] transition-all duration-300"
          :disabled="isLoading"
          @click.prevent="handleSubmit"
        >
          <span v-if="!isLoading">Get Account</span>
          <div v-else class="flex items-center space-x-2">
            <svg
              class="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>Creating account...</span>
          </div>
        </button>

        <p v-if="errorMessage" class="mt-3 text-sm text-red-500 text-center">
          {{ errorMessage }}
        </p>

        <p v-if="successMessage" class="mt-3 text-sm text-green-600 text-center">
          {{ successMessage }}
        </p>

        <p class="mt-4 text-center text-sm">
          Already have an account?
          <a
            href=""
            class="text-[#075e54] font-semibold mb-4"
            @click="redirectLogin"
            >Login</a
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import zxcvbn from "zxcvbn";

export default {
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      turnstileSiteKey:
        process.env.VUE_APP_TURNSTILE_SITE_KEY || "1x00000000000000000000AA",
      turnstileWidgetId: null,
      username: "",
      email: "",
      password: "",
      errorMessage: "",
      successMessage: "",
      isLoading: false,
    };
  },
  name: "BasicSignUpForm",
  computed: {
    strengthScore() {
      return zxcvbn(this.password || "").score;
    },
    strengthLabel() {
      return ["Very Weak", "Weak", "Fair", "Good", "Strong"][
        this.strengthScore
      ];
    },
    strengthColor() {
      return ["#e53e3e", "#dd6b20", "#d69e2e", "#38a169", "#3182ce"][
        this.strengthScore
      ];
    },
    strengthWidth() {
      return `${(this.strengthScore / 4) * 100}%`;
    },
  },
  mounted() {
    const existingScript = document.querySelector(
      'script[src="https://challenges.cloudflare.com/turnstile/v0/api.js"]'
    );

    const renderTurnstile = () => {
      if (window?.turnstile?.render && this.$refs.turnstileContainer) {
        if (this.turnstileWidgetId) {
          window.turnstile.remove(this.turnstileWidgetId);
          this.turnstileWidgetId = null;
        }

        this.turnstileWidgetId = window.turnstile.render(
          this.$refs.turnstileContainer,
          {
            sitekey: this.turnstileSiteKey,
            theme: "light",
          }
        );
      }
    };

    if (existingScript) {
      if (window?.turnstile) {
        renderTurnstile();
      } else {
        existingScript.addEventListener("load", renderTurnstile, {
          once: true,
        });
      }
    } else {
      const script = document.createElement("script");
      script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
      script.async = true;
      script.defer = true;
      script.onload = renderTurnstile;
      document.head.appendChild(script);
    }
  },
  methods: {
    async handleSubmit() {
      this.errorMessage = "";
      this.successMessage = "";

      const token =
        window?.turnstile?.getResponse?.(this.turnstileWidgetId) ||
        document.querySelector('input[name="cf-turnstile-response"]')?.value;

      if (!token) {
        this.errorMessage = "Please complete the CAPTCHA.";
        return;
      }

      if (!this.username || !this.email || !this.password) {
        this.errorMessage = "Please fill in all required fields.";
        return;
      }

      const payload = {
        username: this.username,
        email: this.email,
        password: this.password,
        cf_token: token,
      };

      this.isLoading = true;

      try {
        const baseUrl = this.apiUrl?.trim();
        const sanitizedBase = baseUrl?.replace(/\/+$/, "") || "";
        const registerEndpoint = sanitizedBase
          ? `${sanitizedBase}/register`
          : "/api/register";

        const response = await fetch(registerEndpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

  const rawPayload = await response.text();
        let responseBody = null;

        if (rawPayload) {
          try {
            responseBody = JSON.parse(rawPayload);
          } catch (_error) {
            responseBody = null;
          }
        }

        if (!response.ok) {
          const lowerPayload = rawPayload?.toLowerCase() || "";
          const fallbackMessage = lowerPayload.includes("cloudflare")
            ? lowerPayload.includes("invalid domain")
              ? "This Cloudflare Turnstile key isn't authorized for this domain. Update your site key or switch to the Cloudflare test keys for local development."
              : "The request was blocked by Cloudflare. Ask the backend team to allow this origin or use the approved domain."
            : "Failed to create account. Please try again.";

          const detail = responseBody?.detail;
          const messageFromDetail =
            typeof detail === "string"
              ? detail
              : detail?.message || detail?.turnstile?.message;

          const message =
            messageFromDetail ||
            responseBody?.message ||
            fallbackMessage;

          throw new Error(message);
        }

        if (!responseBody?.success) {
          const feedback =
            responseBody?.detail ||
            responseBody?.message ||
            "Failed to create account. Please try again.";
          throw new Error(feedback);
        }

        this.successMessage =
          responseBody?.message || "Account created successfully!";
        this.username = "";
        this.email = "";
        this.password = "";

        if (window?.turnstile?.reset) {
          if (this.turnstileWidgetId) {
            window.turnstile.reset(this.turnstileWidgetId);
          } else {
            window.turnstile.reset();
          }
        }

        setTimeout(() => {
          this.$router.push("/");
        }, 1200);
      } catch (error) {
        console.error("Error creating account:", error);
        this.errorMessage =
          error?.message || "Something went wrong. Please try again.";
      } finally {
        this.isLoading = false;
      }
    },
    redirectLogin() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.logo {
  font-weight: 800;
  margin: 8px 0;
  padding-right: 30px;
  font-size: 30px;
  color: #075e54;
}
.bg-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-image: url("@/assets/LoginPage.png");
  background-position: center;
  padding: 0 16px;
}

@media (min-width: 640px) {
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 32px;
  }
}
</style>
