from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import TextQL


class Playbooks:
    def __init__(self, client: TextQL) -> None:
        self._client = client

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search_term: str | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
        status_filter: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search_term is not None:
            params["search_term"] = search_term
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_direction is not None:
            params["sort_direction"] = sort_direction
        if status_filter is not None:
            params["status_filter"] = status_filter
        return self._client._request("GET", "/v2/playbooks", params=params)

    def create(self) -> Any:
        return self._client._request("POST", "/v2/playbooks")

    def get(
        self,
        playbook_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._client._request("GET", f"/v2/playbooks/{playbook_id}", params=params)

    def update(
        self,
        playbook_id: str,
        *,
        name: str | None = None,
        prompt: str | None = None,
        cron_string: str | None = None,
        connector_ids: list[int] | None = None,
        dataset_ids: list[str] | None = None,
        email_addresses: list[str] | None = None,
        slack_channel_id: str | None = None,
        tagged_slack_user_ids: list[str] | None = None,
        selected_template_data_ids: list[str] | None = None,
    ) -> Any:
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if prompt is not None:
            body["prompt"] = prompt
        if cron_string is not None:
            body["cron_string"] = cron_string
        if connector_ids is not None:
            body["connector_ids"] = connector_ids
        if dataset_ids is not None:
            body["dataset_ids"] = dataset_ids
        if email_addresses is not None:
            body["email_addresses"] = email_addresses
        if slack_channel_id is not None:
            body["slack_channel_id"] = slack_channel_id
        if tagged_slack_user_ids is not None:
            body["tagged_slack_user_ids"] = tagged_slack_user_ids
        if selected_template_data_ids is not None:
            body["selected_template_data_ids"] = selected_template_data_ids
        return self._client._request("PATCH", f"/v2/playbooks/{playbook_id}", json=body)

    def deploy(self, playbook_id: str) -> Any:
        return self._client._request("POST", f"/v2/playbooks/{playbook_id}/deploy")

    def delete(self, playbook_id: str) -> Any:
        return self._client._request("DELETE", f"/v2/playbooks/{playbook_id}")

    def run(self, playbook_id: str, *, dry_run: bool = False) -> Any:
        body: dict[str, Any] = {}
        if dry_run:
            body["dry_run"] = True
        return self._client._request("POST", f"/v2/playbooks/{playbook_id}/run", json=body)
