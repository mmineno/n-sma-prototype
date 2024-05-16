# spec/controllers/dashboard_controller_spec.rb
require 'rails_helper'

RSpec.describe DashboardController, type: :controller do
  describe "GET #index" do
    let(:user) { create(:user) }

    before do
      sign_in user
    end

    it "returns a successful response" do
      get :index
      expect(response).to be_successful
    end

    it "assigns the current user" do
      get :index
      expect(assigns(:user)).to eq(user)
    end

    it "assigns notifications" do
      notification = create(:notification, user: user)
      get :index
      expect(assigns(:notifications)).to include(notification)
    end

    it "assigns today schedules" do
      schedule = create(:schedule, user: user)
      get :index
      expect(assigns(:today_schedules)).to include(schedule)
    end

    it "assigns pending documents" do
      document = create(:document, user: user)
      get :index
      expect(assigns(:pending_documents)).to include(document)
    end

    it "assigns menu items" do
      menu_item = create(:menu_item)
      get :index
      expect(assigns(:menu_items)).to include(menu_item)
    end
  end
end
