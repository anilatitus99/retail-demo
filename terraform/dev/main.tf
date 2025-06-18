provider "google" {
  project = "retail-1234"  
  region  = "us-central1"
}

resource "google_artifact_registry_repository" "repo" {
  provider = google
  location     = "us-central1"
  repository_id = "retail-repo"
  format       = "DOCKER"
  description  = "Artifact Registry for retail project"
}

resource "google_cloud_run_service" "products" {
  name     = "products"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/retail-1234/retail-repo/products:dev"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  location        = google_cloud_run_service.products.location
  service         = google_cloud_run_service.products.name
  role            = "roles/run.invoker"
  member          = "allUsers"
}

resource "google_cloud_run_service" "inventory" {
  name     = "inventory"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/retail-1234/retail-repo/inventory:latest"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "inventory_invoker" {
  location = google_cloud_run_service.inventory.location
  service  = google_cloud_run_service.inventory.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service" "orders" {
  name     = "orders"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/retail-1234/retail-repo/orders:dev"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "orders_invoker" {
  location = google_cloud_run_service.orders.location
  service  = google_cloud_run_service.orders.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
