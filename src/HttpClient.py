import requests
from typing import Dict, Optional, Union
import json
import time


class HttpClient:
    """
    标准化 HTTP 客户端封装，支持 GET/POST 请求，包含异常处理和通用配置
    """

    def __init__(
            self,
            base_url: str = "",
            timeout: int = 10,
            headers: Optional[Dict[str, str]] = None,
            verify_ssl: bool = True
    ):
        """
        初始化 HTTP 客户端

        :param base_url: API 基础 URL（如 "https://api.example.com"）
        :param timeout: 请求超时时间（秒）
        :param headers: 默认请求头（如认证信息）
        :param verify_ssl: 是否验证 SSL 证书（生产环境建议保持 True）
        """
        self.base_url = base_url.rstrip("/") + "/"  # 统一处理斜杠
        self.timeout = timeout
        self.headers = headers or {}
        self.verify_ssl = verify_ssl
        self.session = requests.Session()  # 使用 Session 保持连接（提升性能）

    def _handle_response(self, response: requests.Response) -> Union[Dict, str]:
        """
        统一处理响应结果，优先尝试解析 JSON，失败返回文本

        :param response: requests 响应对象
        :return: 解析后的 JSON 数据或原始文本
        """
        try:
            # 尝试解析 JSON（适用于接口返回 JSON 的场景）
            if response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            # 非 JSON 响应返回原始文本
            return response.text
        except json.JSONDecodeError:
            return response.text

    def get(
            self,
            endpoint: str,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            timeout: Optional[int] = None
    ) -> Union[Dict, str, None]:
        """
        发送 GET 请求

        :param endpoint: API 端点（如 "/user/info"）
        :param params: 查询参数（自动拼接至 URL）
        :param headers: 覆盖默认请求头（可选）
        :param timeout: 覆盖默认超时时间（可选）
        :return: 解析后的响应数据（JSON/文本）或 None（请求失败）
        """
        url = f"{self.base_url}{endpoint.lstrip('/')}"
        try:
            # 合并请求头（优先使用传入的 headers）
            request_headers = {**self.headers, **(headers or {})}

            response = self.session.get(
                url=url,
                params=params,
                headers=request_headers,
                timeout=timeout or self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()  # 若状态码非 2xx 则抛出异常

            return self._handle_response(response)

        except requests.exceptions.HTTPError as e:
            print(f"HTTP 请求失败（状态码 {response.status_code}）: {str(e)}")
        except requests.exceptions.ConnectionError:
            print("连接失败：请检查网络或目标地址是否可用")
        except requests.exceptions.Timeout:
            print(f"请求超时（超时时间 {timeout or self.timeout} 秒）")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {str(e)}")
        except Exception as e:
            print(f"未知错误: {str(e)}")
        return None

    def post(
            self,
            endpoint: str,
            data: Optional[Union[Dict, str]] = None,
            json_data: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            timeout: Optional[int] = None
    ) -> Union[Dict, str, None]:
        """
        发送 POST 请求（支持表单数据或 JSON 数据）

        :param endpoint: API 端点（如 "/user/create"）
        :param data: 表单数据（字典或字符串，自动编码为 form-data）
        :param json_data: JSON 数据（字典，自动序列化为 JSON）
        :param headers: 覆盖默认请求头（可选）
        :param timeout: 覆盖默认超时时间（可选）
        :return: 解析后的响应数据（JSON/文本）或 None（请求失败）
        """
        url = f"{self.base_url}{endpoint.lstrip('/')}"
        try:
            request_headers = {**self.headers,** (headers or {})}

            response = self.session.post(
                url=url,
                data=data,
                json=json_data,
                headers=request_headers,
                timeout=timeout or self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()

            return self._handle_response(response)

        except requests.exceptions.HTTPError as e:
            print(f"HTTP 请求失败（状态码 {response.status_code}）: {str(e)}")
        except requests.exceptions.ConnectionError:
            print("连接失败：请检查网络或目标地址是否可用")
        except requests.exceptions.Timeout:
            print(f"请求超时（超时时间 {timeout or self.timeout} 秒）")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {str(e)}")
        except Exception as e:
            print(f"未知错误: {str(e)}")
        return None

    def close(self):
        """关闭 Session 连接（释放资源）"""
        self.session.close()

    def delete(
            self,
            endpoint: str,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            data: Optional[Union[Dict, str]] = None,
            timeout: Optional[int] = None
    ) -> Union[Dict, str, None]:
        """
        发送 DELETE 请求

        :param endpoint: API 端点（如 "/resource/123"）
        :param params: URL 查询参数
        :param headers: 覆盖默认请求头
        :param data: 请求体数据（JSON 或原始字符串）
        :param timeout: 覆盖默认超时时间
        :return: 解析后的 JSON 或原始文本，失败返回 None
        """
        url = f"{self.base_url}{endpoint.lstrip('/')}"
        try:
            request_headers = {**self.headers,** (headers or {})}

            response = self.session.delete(
                url=url,
                params=params,
                headers=request_headers,
                data=data,
                timeout=timeout or self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()  # 自动抛出 HTTP 错误

            return self._handle_response(response)

        except requests.exceptions.HTTPError as e:
            print(f"HTTP 错误 [{response.status_code}]: {str(e)}")
        except requests.exceptions.ConnectionError:
            print("连接失败，请检查网络或目标地址")
        except requests.exceptions.Timeout:
            print(f"请求超时 ({timeout or self.timeout} 秒)")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {str(e)}")
        return None
