"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import os

def api_root(request):
    """Root endpoint showing available API endpoints"""
    codespace_name = os.environ.get('CODESPACE_NAME')
    base_url = f'https://{codespace_name}-8000.app.github.dev' if codespace_name else 'http://localhost:8000'
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OctoFit Tracker API</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 800px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            .version {{
                color: #888;
                margin-bottom: 30px;
                font-size: 0.9em;
            }}
            .description {{
                color: #555;
                margin-bottom: 30px;
                line-height: 1.6;
            }}
            .endpoints {{
                display: grid;
                gap: 15px;
            }}
            .endpoint {{
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px 20px;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            .endpoint:hover {{
                background: #e9ecef;
                transform: translateX(5px);
            }}
            .endpoint-name {{
                font-weight: 600;
                color: #333;
                margin-bottom: 5px;
                font-size: 1.1em;
            }}
            .endpoint-url {{
                color: #667eea;
                text-decoration: none;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                word-break: break-all;
            }}
            .endpoint-url:hover {{
                text-decoration: underline;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
                text-align: center;
                color: #888;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏋️ OctoFit Tracker API</h1>
            <div class="version">Version 1.0</div>
            <div class="description">
                Welcome to the OctoFit Tracker REST API! This API provides endpoints for managing fitness tracking, 
                team management, activity logging, leaderboards, and personalized workout suggestions.
            </div>
            
            <div class="endpoints">
                <div class="endpoint">
                    <div class="endpoint-name">👥 Users</div>
                    <a href="{base_url}/api/users/" class="endpoint-url">{base_url}/api/users/</a>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-name">🏆 Teams</div>
                    <a href="{base_url}/api/teams/" class="endpoint-url">{base_url}/api/teams/</a>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-name">🏃 Activities</div>
                    <a href="{base_url}/api/activities/" class="endpoint-url">{base_url}/api/activities/</a>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-name">📊 Leaderboard</div>
                    <a href="{base_url}/api/leaderboard/" class="endpoint-url">{base_url}/api/leaderboard/</a>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-name">💪 Workouts</div>
                    <a href="{base_url}/api/workouts/" class="endpoint-url">{base_url}/api/workouts/</a>
                </div>
                
                <div class="endpoint">
                    <div class="endpoint-name">⚙️ Admin Panel</div>
                    <a href="{base_url}/admin/" class="endpoint-url">{base_url}/admin/</a>
                </div>
            </div>
            
            <div class="footer">
                Built with Django REST Framework • MongoDB • React
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
