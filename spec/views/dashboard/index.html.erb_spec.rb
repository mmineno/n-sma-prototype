# spec/views/dashboard/index.html.erb_spec.rb
require 'rails_helper'

RSpec.describe "dashboard/index.html.erb", type: :view do
  let(:user) { create(:user) }
  let(:notification) { create(:notification, user: user) }
  let(:schedule) { create(:schedule, user: user) }
  let(:document) { create(:document, user: user) }
  let(:menu_item) { create(:menu_item) }

  before do
    assign(:user, user)
    assign(:notifications, [notification])
    assign(:today_schedules, [schedule])
    assign(:pending_documents, [document])
    assign(:menu_items, [menu_item])
  end

  it "displays the user's name and greeting message" do
    render
    expect(rendered).to include(user.name)
    expect(rendered).to include(user.greeting_message)
  end

  it "displays notifications" do
    render
    expect(rendered).to include(notification.title)
    expect(rendered).to include(notification.content)
  end

  it "displays today's schedules" do
    render
    expect(rendered).to include(schedule.title)
  end

  it "displays pending documents" do
    render
    expect(rendered).to include(document.document_type)
    expect(rendered).to include(document.updated_by)
  end

  it "displays menu items" do
    render
    expect(rendered).to include(menu_item.name)
  end
end
