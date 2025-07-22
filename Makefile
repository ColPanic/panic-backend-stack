# AI Backend Services Stack
# A complete backend infrastructure for AI applications

# Load environment variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Docker Compose configuration
COMPOSE_FILE := docker-compose.yml
COMPOSE_CMD := docker compose -f $(COMPOSE_FILE)

.PHONY: help setup up down restart status health logs shell-db shell-redis backup restore clean

help: ## Show this help
	@echo "AI Backend Services Stack - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' '{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Service URLs (after starting):"
	@echo "  PostgreSQL:     localhost:5432"
	@echo "  Redis:          localhost:6379"
	@echo "  ChromaDB:       http://localhost:8000"
	@echo "  MinIO API:      http://localhost:9000"
	@echo "  MinIO Console:  http://localhost:9001"
	@echo "  Health Check:   http://localhost/health"

setup: ## First-time setup - create .env file and directories
	@echo "🚀 Setting up AI Backend Services..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file from template"; \
		echo "⚠️  Please edit .env with your desired passwords and settings"; \
	else \
		echo "ℹ️  .env file already exists"; \
	fi
	@mkdir -p backups
	@echo "🎉 Setup complete!"

up: ## Start all backend services
	@echo "🚀 Starting AI Backend Services..."
	$(COMPOSE_CMD) up -d
	@echo "✅ AI Backend Services started successfully"
	@echo ""
	@echo "📊 Service URLs:"
	@echo "  🐘 PostgreSQL:     localhost:${POSTGRES_PORT:-5432}"
	@echo "  🟥 Redis:          localhost:${REDIS_PORT:-6379}"
	@echo "  🔍 ChromaDB:       http://localhost:${CHROMA_PORT:-8000}"
	@echo "  📦 MinIO API:      http://localhost:${MINIO_API_PORT:-9000}"
	@echo "  🌐 MinIO Console:  http://localhost:${MINIO_CONSOLE_PORT:-9001}"
	@echo "  🏥 Health Check:   http://localhost:${NGINX_HTTP_PORT:-80}/health"
	@echo ""
	@echo "💡 Use 'make health' to check service status"
	@echo "💡 Use 'make logs' to view service logs"

down: ## Stop all backend services
	@echo "⛔ Stopping AI Backend Services..."
	$(COMPOSE_CMD) down
	@echo "✅ AI Backend Services stopped"

restart: ## Restart all backend services
	@echo "🔄 Restarting AI Backend Services..."
	$(COMPOSE_CMD) restart
	@echo "✅ AI Backend Services restarted"

status: ## Show service status and resource usage
	@echo "📊 AI Backend Services Status:"
	@$(COMPOSE_CMD) ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "💾 Resource usage:"
	@docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" \
		ai-postgres ai-redis ai-chromadb ai-minio ai-nginx 2>/dev/null || echo "Some containers not running"

health: ## Check health of all services
	@echo "🏥 Checking AI Backend Services health..."
	@echo "🐘 PostgreSQL:"
	@docker exec ai-postgres pg_isready -U ${POSTGRES_USER:-ai_user} -d ${POSTGRES_DB:-ai_app} 2>/dev/null && echo "   ✅ Ready" || echo "   ❌ Not ready"
	@echo "🟥 Redis:"
	@docker exec ai-redis redis-cli ping 2>/dev/null && echo "   ✅ Ready" || echo "   ❌ Not ready"
	@echo "🔍 ChromaDB:"
	@curl -f -s http://localhost:${CHROMA_PORT:-8000}/api/v1/heartbeat > /dev/null 2>&1 && echo "   ✅ Ready" || echo "   ❌ Not ready"
	@echo "📦 MinIO:"
	@curl -f -s http://localhost:${MINIO_API_PORT:-9000}/minio/health/live > /dev/null 2>&1 && echo "   ✅ Ready" || echo "   ❌ Not ready"
	@echo "🌐 Nginx:"
	@curl -f -s http://localhost:${NGINX_HTTP_PORT:-80}/health > /dev/null 2>&1 && echo "   ✅ Ready" || echo "   ❌ Not ready"

logs: ## View logs from all services
	@echo "📋 Following all service logs (Ctrl+C to exit)..."
	$(COMPOSE_CMD) logs -f --tail=100

logs-postgres: ## View PostgreSQL logs
	@echo "🐘 PostgreSQL logs:"
	$(COMPOSE_CMD) logs --tail=50 postgres

logs-redis: ## View Redis logs
	@echo "🟥 Redis logs:"
	$(COMPOSE_CMD) logs --tail=50 redis

logs-chromadb: ## View ChromaDB logs
	@echo "🔍 ChromaDB logs:"
	$(COMPOSE_CMD) logs --tail=50 chromadb

logs-minio: ## View MinIO logs
	@echo "📦 MinIO logs:"
	$(COMPOSE_CMD) logs --tail=50 minio

shell-db: ## Open PostgreSQL shell
	@echo "🐘 Opening PostgreSQL shell..."
	docker exec -it ai-postgres psql -U ${POSTGRES_USER:-ai_user} -d ${POSTGRES_DB:-ai_app}

shell-redis: ## Open Redis CLI
	@echo "🟥 Opening Redis CLI..."
	docker exec -it ai-redis redis-cli

backup: ## Backup PostgreSQL database
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	docker exec ai-postgres pg_dump -U ${POSTGRES_USER:-ai_user} -d ${POSTGRES_DB:-ai_app} > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Database backup created in backups/"

restore: ## Restore PostgreSQL database from backup (usage: make restore BACKUP=backups/backup_YYYYMMDD_HHMMSS.sql)
	@if [ -z "$(BACKUP)" ]; then \
		echo "❌ Please specify backup file: make restore BACKUP=backups/backup_YYYYMMDD_HHMMSS.sql"; \
		exit 1; \
	fi
	@echo "📥 Restoring database from $(BACKUP)..."
	docker exec -i ai-postgres psql -U ${POSTGRES_USER:-ai_user} -d ${POSTGRES_DB:-ai_app} < $(BACKUP)
	@echo "✅ Database restored successfully"

clean: ## Remove stopped containers and unused volumes
	@echo "🧹 Cleaning up containers and volumes..."
	$(COMPOSE_CMD) down --remove-orphans
	docker system prune -f --volumes
	@echo "✅ Cleanup completed"

reset-minio: ## Reset MinIO credentials (fixes login issues)
	@echo "🔄 Resetting MinIO credentials..."
	@echo "⚠️  This will delete all MinIO data!"
	@read -p "Are you sure? [y/N]: " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(COMPOSE_CMD) stop minio; \
		$(COMPOSE_CMD) rm -f minio; \
		docker volume rm ai-backend-stack_minio_data 2>/dev/null || true; \
		$(COMPOSE_CMD) up -d minio; \
		echo "✅ MinIO reset with fresh credentials"; \
		echo "🔑 Login at http://localhost:${MINIO_CONSOLE_PORT:-9001}"; \
		echo "   Username: ${MINIO_ROOT_USER:-ai_admin}"; \
		echo "   Password: ${MINIO_ROOT_PASSWORD:-ai_minio_password}"; \
	else \
		echo "❌ Operation cancelled"; \
	fi

# Development shortcuts
dev-up: up ## Alias for 'up'
dev-down: down ## Alias for 'down'
start: up ## Alias for 'up' 
stop: down ## Alias for 'down'