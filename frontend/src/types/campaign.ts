export interface CampaignBrief {
  business_name: string;
  business_type: string;
  target_audience: string;
  campaign_goal: string;
  key_messages: string;
  tone: string;
  platforms: string[];
  include_hashtags: boolean;
  include_emoji: boolean;
  seasonal_hook: string | null;
}

export interface PlatformCopy {
  platform: string;
  copy: string;
  character_count: number;
}

export interface CampaignResponse {
  success: boolean;
  business_name: string;
  copies: PlatformCopy[];
  image_prompt: string;
  image_url: string | null;
  revised_image_prompt: string | null;
  message: string | null;
}

export interface ApiError {
  detail: string;
}

export const AVAILABLE_PLATFORMS = [
  "Instagram",
  "Facebook",
  "LinkedIn",
  "X",
  "TikTok",
] as const;

export const TONE_OPTIONS = [
  "friendly and professional",
  "warm and inviting",
  "playful and fun",
  "luxurious and sophisticated",
  "casual and relaxed",
  "urgent and exciting",
] as const;

export const UK_SEASONAL_HOOKS = [
  "Spring",
  "Summer",
  "Autumn",
  "Winter",
  "New Year",
  "Valentine's Day",
  "Mother's Day",
  "Easter",
  "Father's Day",
  "Bank Holiday Weekend",
  "Summer Holidays",
  "Back to School",
  "Halloween",
  "Bonfire Night",
  "Black Friday",
  "Christmas",
  "Boxing Day",
] as const;
