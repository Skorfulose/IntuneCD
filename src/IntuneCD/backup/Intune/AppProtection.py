# -*- coding: utf-8 -*-
from ...intunecdlib.BaseBackupModule import BaseBackupModule


class AppProtectionBackupModule(BaseBackupModule):
    """A class used to backup Intune App Protection

    Attributes:
        CONFIG_ENDPOINT (str): The endpoint to get the data from
        LOG_MESSAGE (str): The message to log when backing up the data
    """

    CONFIG_ENDPOINT = "/beta/deviceAppManagement/managedAppPolicies"
    LOG_MESSAGE = "Backing up App Protection: "

    def __init__(self, *args, **kwargs):
        """Initializes the AppProtectionBackupModule class

        Args:
            *args: The positional arguments to pass to the base class's __init__ method.
            **kwargs: The keyword arguments to pass to the base class's __init__ method.
        """
        super().__init__(*args, **kwargs)
        self.path = f"{self.path}/App Protection/"
        self.audit_filter = (
            self.audit_filter or "componentName eq 'ManagedAppProtection'"
        )
        self.assignment_endpoint = self.assignment_endpoint or "deviceAppManagement/"
        self.assignment_extra_url = self.assignment_extra_url or "/assignments"
        self.app_protection = True

    def main(self) -> dict[str, any]:
        """The main method to backup the App Protections

        Returns:
            dict[str, any]: The results of the backup
        """
        try:
            self.graph_data = self.make_graph_request(
                endpoint=self.endpoint + self.CONFIG_ENDPOINT
            )
        except Exception as e:
            self.log(
                msg=f"Error getting App Protection data from {self.endpoint + self.CONFIG_ENDPOINT}: {e}"
            )
            return None

        try:
            self.results = self.process_data(
                data=self.graph_data["value"],
                filetype=self.filetype,
                path=self.path,
                name_key="displayName",
                log_message=self.LOG_MESSAGE,
                audit_compare_info={"type": "resourceId", "value_key": "id"},
            )
        except Exception as e:
            self.log(msg=f"Error processing App Protection data: {e}")
            return None

        return self.results
